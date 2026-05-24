"""
IMDConnector: India Meteorological Department district-level weather data.

The IMD rainfall page embeds district data as JavaScript objects inside the
page HTML. This connector parses that embedded data alongside a district-to-state
mapping fetched from IMD's own GeoJSON file and requires no headless browser.

Run directly to see sample output:
    PYTHONPATH=. python3 connectors/imd/connector.py
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import re
from datetime import datetime, timezone

import requests

from connectors.base_connector import (
    BaseConnector,
    ConnectorFetchError,
    ConnectorMetadata,
    ValidationResult,
)
from schema.models import KalkiLocation, KalkiRecord, Module

logger = logging.getLogger(__name__)

IMD_BASE_URL = "https://mausam.imd.gov.in/responsive/rainfallinformation.php"
IMD_URL = f"{IMD_BASE_URL}?msg=D"

GEOJSON_URL = (
    "https://mausam.imd.gov.in/imd_latest/contents/district_shapefiles/india_gj_2024.geojson"
)

_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; KalkiBot/0.1)"}


class IMDConnector(BaseConnector):
    """
    Connector for IMD district-level daily rainfall.

    fetch() returns a dict with two keys:
      - "html":      raw HTML bytes from the IMD rainfall page
      - "state_map": dict[district_uppercase -> state_titlecase] built from
                     IMD's own district GeoJSON file

    validate() inspects the HTML portion only.
    to_standard_schema() uses both to emit one KalkiRecord per district.
    """

    VERSION = "0.1.0"

    def get_metadata(self) -> ConnectorMetadata:
        return ConnectorMetadata(
            name="IMD District Weather Connector",
            source_name="India Meteorological Department",
            source_url=IMD_URL,
            module=Module.PRAKRITI,
            version=self.VERSION,
            update_frequency="daily",
            data_format="HTML scrape (embedded JS) + GeoJSON state lookup",
            caveats=[
                "IMD does not expose a clean REST API; rainfall data is extracted "
                "from JavaScript embedded in the page HTML.",
                "District names are stored uppercase in IMD data and may not match "
                "LGD canonical names: district_lgd_code is provided for reliable joins.",
                "Temperature and humidity are not available at the district level from "
                "any public IMD endpoint. See README.md for a full investigation summary.",
                "State names are resolved via IMD's district GeoJSON; unmatched districts "
                "fall back to 'India'.",
            ],
        )

    def fetch(self) -> dict:
        """
        Fetch rainfall HTML and district-state mapping in one pass.

        Returns:
            {
              "html":      bytes   : raw HTML from the IMD daily rainfall page
              "state_map": dict    : {DISTRICT_UPPERCASE: "State Titlecase"}
            }
        """
        try:
            resp = requests.get(IMD_URL, timeout=30, headers=_HEADERS)
            resp.raise_for_status()
            html_bytes = resp.content
        except requests.RequestException as exc:
            raise ConnectorFetchError(f"Failed to fetch IMD rainfall data: {exc}") from exc

        state_map: dict[str, str] = {}
        try:
            geo = requests.get(GEOJSON_URL, timeout=60, headers=_HEADERS)
            geo.raise_for_status()
            features = geo.json().get("features", [])
            for f in features:
                props = f.get("properties") or {}
                district = props.get("District", "").strip()
                state = props.get("STATE", "").strip()
                if district and state:
                    state_map[district] = state.title()
            logger.info("State map loaded: %d district entries", len(state_map))
        except Exception as exc:
            logger.warning(
                "Could not load district-state GeoJSON: %s : state will default to 'India'",
                exc,
            )

        return {"html": html_bytes, "state_map": state_map}

    def validate(self, raw: dict) -> ValidationResult:
        """Check that the HTML portion contains embedded district rainfall data."""
        issues: list[str] = []
        warnings: list[str] = []

        html: bytes = raw.get("html", b"")

        if not html:
            issues.append("Empty response received from IMD")
            return ValidationResult(is_valid=False, issues=issues)

        text = html.decode("utf-8", errors="replace")

        if '"areas"' not in text:
            issues.append(
                'Expected "areas" JS key not found: IMD page structure may have changed'
            )

        if '"balloonText"' not in text:
            issues.append(
                'Expected "balloonText" JS key not found: IMD page structure may have changed'
            )

        if "Actual" not in text or "mm" not in text:
            warnings.append(
                "Could not find rainfall values in page: verify IMD URL is correct"
            )

        if not raw.get("state_map"):
            warnings.append(
                "District-state mapping is empty: state field will be 'India' for all records"
            )

        return ValidationResult(is_valid=len(issues) == 0, issues=issues, warnings=warnings)

    def to_standard_schema(self, raw: dict) -> list[KalkiRecord]:
        """Extract district rainfall from embedded JS and emit KalkiRecords."""
        html: bytes = raw.get("html", b"")
        state_map: dict[str, str] = raw.get("state_map", {})

        source_hash = hashlib.sha256(html).hexdigest()
        fetch_time = datetime.now(tz=timezone.utc)

        text = html.decode("utf-8", errors="replace")
        areas = _extract_areas(text)
        if not areas:
            logger.warning("No district areas found in IMD page")
            return []

        records: list[KalkiRecord] = []

        for area in areas:
            district_upper = area.get("title", "").strip()
            lgd_code = area.get("id", "").strip()
            balloon = area.get("balloonText", "")

            if not district_upper or not balloon:
                continue

            date_str = _parse_balloon(balloon, r"Date\s*:\s*([\d-]+)")
            actual_str = _parse_balloon(balloon, r"Actual\s*:\s*([\d.]+)\s*mm")

            if not date_str or not actual_str:
                logger.debug("Skipping %s: no date or rainfall value", district_upper)
                continue

            try:
                record_time = datetime.fromisoformat(date_str).replace(tzinfo=timezone.utc)
            except ValueError:
                logger.warning("Bad date for %s: %r", district_upper, date_str)
                continue

            rainfall_mm = _safe_float(actual_str)
            if rainfall_mm is None:
                logger.debug("Skipping %s: unparseable rainfall value", district_upper)
                continue

            # Resolve state from GeoJSON mapping; fall back to "India" if not found
            state = state_map.get(district_upper, "India")

            data_payload = {
                "rainfall_mm": rainfall_mm,
                "temperature_max_c": None,   # not available at district level from IMD
                "temperature_min_c": None,   # not available at district level from IMD
                "humidity_pct": None,        # not available at district level from IMD
            }

            location = KalkiLocation(
                state=state,
                district=district_upper.title(),
                district_lgd_code=lgd_code or None,
            )

            records.append(
                KalkiRecord(
                    source_name="India Meteorological Department",
                    source_url=IMD_URL,
                    connector_version=self.VERSION,
                    module=Module.PRAKRITI,
                    location=location,
                    record_timestamp=record_time,
                    fetch_timestamp=fetch_time,
                    data=data_payload,
                    data_quality_score=self._compute_quality_score(data_payload),
                    raw_source_hash=source_hash,
                )
            )

        return records

    def _compute_quality_score(self, data: dict) -> float:
        """
        Composite quality score (0.0–1.0) using Kalki 5-dimension framework.

        Weights: Completeness 30%, Timeliness 25%, Consistency 20%,
                 Accuracy 15%, Provenance 10%.
        """
        expected = {"rainfall_mm", "temperature_max_c", "temperature_min_c", "humidity_pct"}
        present = sum(1 for f in expected if data.get(f) is not None)
        completeness = (present / len(expected)) * 0.30

        timeliness = 1.0 * 0.25  # daily data fetched same day

        consistent = True
        if (v := data.get("temperature_max_c")) is not None and not (0 <= v <= 60):
            consistent = False
        if (v := data.get("temperature_min_c")) is not None and not (-10 <= v <= 50):
            consistent = False
        if (v := data.get("humidity_pct")) is not None and not (0 <= v <= 100):
            consistent = False
        if (v := data.get("rainfall_mm")) is not None and v < 0:
            consistent = False
        consistency = (1.0 if consistent else 0.5) * 0.20

        accuracy = 0.5 * 0.15   # no cross-validation available
        provenance = 1.0 * 0.10  # stable government source

        return round(completeness + timeliness + consistency + accuracy + provenance, 3)


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------

def _extract_areas(text: str) -> list[dict]:
    """
    Extract the 'areas' JSON array from embedded JavaScript in IMD page HTML.

    The array is bracket-counted so it handles any size without regex limits.
    """
    marker = '"areas": ['
    start_idx = text.find(marker)
    if start_idx == -1:
        return []

    arr_start = start_idx + len(marker) - 1  # index of opening '['
    depth = 0
    pos = arr_start

    while pos < len(text):
        c = text[pos]
        if c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                break
        pos += 1
    else:
        logger.warning("Unmatched '[' in IMD areas array")
        return []

    try:
        return json.loads(text[arr_start : pos + 1])
    except json.JSONDecodeError as exc:
        logger.warning("Could not parse IMD areas JSON: %s", exc)
        return []


def _parse_balloon(balloon: str, pattern: str) -> str | None:
    """Extract first capture group matching pattern from an IMD balloonText."""
    m = re.search(pattern, balloon)
    return m.group(1) if m else None


def _safe_float(val: object) -> float | None:
    """Return float(val) or None if conversion fails or value is NaN."""
    try:
        result = float(val)
        return None if math.isnan(result) else result
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Quick smoke-test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    connector = IMDConnector()

    print("\n=== Connector Metadata ===")
    meta = connector.get_metadata()
    print(f"Name:      {meta.name}")
    print(f"Source:    {meta.source_name}")
    print(f"Module:    {meta.module.value}")
    print(f"Version:   {meta.version}")
    print(f"Caveats:   {meta.caveats[0]}")

    print("\n=== Running connector pipeline ===")
    records = connector.run()

    print(f"\nProduced {len(records)} record(s):\n")
    for r in records[:10]:
        print(f"  District:  {r.location.district}, {r.location.state} (LGD: {r.location.district_lgd_code})")
        print(f"  Date:      {r.record_timestamp.date()}")
        print(f"  Data:      {r.data}")
        print(f"  Quality:   {r.data_quality_score}")
        print(f"  Hash:      {r.raw_source_hash[:16]}...")
        print()
    if len(records) > 10:
        print(f"  ... and {len(records) - 10} more records")
