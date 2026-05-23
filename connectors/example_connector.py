"""
ExampleConnector: a fully-annotated reference implementation.

This connector uses mock data (no real network calls) so you can read,
run, and understand the full connector pattern without any setup.

When building a real connector (e.g. for IMD, NDMA, CPCB):
1. Copy this file into a new directory: connectors/your_source/connector.py
2. Replace the mock fetch() with your real HTTP/scraper logic
3. Replace validate() and to_standard_schema() with source-specific logic
4. Update get_metadata() with accurate details
5. Delete these instructions and write your own docstring

Run this file directly to see sample output:
    python connectors/example_connector.py
"""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import datetime, timezone

from connectors.base_connector import (
    BaseConnector,
    ConnectorMetadata,
    ValidationResult,
)
from schema.models import KalkiLocation, KalkiRecord, Module

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mock data — replace with a real requests.get() call in a live connector
# ---------------------------------------------------------------------------

MOCK_API_RESPONSE = {
    "source": "Mock Meteorological Department",
    "fetched_at": "2026-05-23T10:00:00Z",
    "records": [
        {
            "state": "Odisha",
            "state_code": "IN-OD",
            "district": "Ganjam",
            "district_lgd_code": "373",
            "date": "2026-05-23",
            "rainfall_mm": 42.5,
            "temperature_max_c": 38.2,
            "temperature_min_c": 27.1,
            "humidity_pct": 84,
        },
        {
            "state": "Odisha",
            "state_code": "IN-OD",
            "district": "Puri",
            "district_lgd_code": "374",
            "date": "2026-05-23",
            "rainfall_mm": 18.0,
            "temperature_max_c": 36.5,
            "temperature_min_c": 26.8,
            "humidity_pct": 79,
        },
    ],
}


# ---------------------------------------------------------------------------
# Connector implementation
# ---------------------------------------------------------------------------

class ExampleWeatherConnector(BaseConnector):
    """
    Reference connector demonstrating the full BaseConnector pattern.

    Fetches district-level daily weather observations (mock data).
    In a real connector, fetch() would call the actual IMD API.
    """

    VERSION = "0.1.0"

    def get_metadata(self) -> ConnectorMetadata:
        """
        Describe this connector for the registry.
        Fill in accurate values when building a real connector.
        """
        return ConnectorMetadata(
            name="Example District Weather Connector",
            source_name="Mock Meteorological Department",
            source_url="https://example.com/weather-api",  # real URL in live connectors
            module=Module.PRAKRITI,
            version=self.VERSION,
            maintainer=None,            # your GitHub username once you contribute
            update_frequency="daily",
            data_format="JSON API",
            caveats=[
                "This is a mock connector for development reference only.",
                "Replace with real IMD API endpoint before use.",
            ],
        )

    def fetch(self) -> dict:
        """
        Download raw data from the source.

        In a real connector this would look like:
            import requests
            response = requests.get(
                "https://imd.gov.in/api/district-weather",
                timeout=30,
            )
            response.raise_for_status()
            return response.json()

        Here we return mock data so the example runs without network access.
        """
        logger.info("Fetching mock weather data (no real network call)")
        return MOCK_API_RESPONSE

    def validate(self, raw: dict) -> ValidationResult:
        """
        Check that the raw response is usable.

        Add checks specific to your data source here. Common things to verify:
        - Required top-level keys are present
        - Record count is within expected range
        - Date fields parse correctly
        - No encoding artifacts in string fields
        """
        issues = []
        warnings = []

        # Check required top-level keys
        required_keys = {"source", "fetched_at", "records"}
        missing = required_keys - raw.keys()
        if missing:
            issues.append(f"Missing required keys: {missing}")

        # Check records list is non-empty
        records = raw.get("records", [])
        if not records:
            issues.append("Response contains no records")

        # Check each record has the fields we need
        required_record_keys = {"state", "district", "date"}
        for i, record in enumerate(records):
            missing_in_record = required_record_keys - record.keys()
            if missing_in_record:
                issues.append(
                    f"Record {i} missing fields: {missing_in_record}"
                )

        # Non-blocking: flag records with very high rainfall (may be erroneous)
        for record in records:
            if record.get("rainfall_mm", 0) > 200:
                warnings.append(
                    f"District {record.get('district')} reports "
                    f"{record['rainfall_mm']}mm rainfall — verify this value."
                )

        return ValidationResult(
            is_valid=len(issues) == 0,
            issues=issues,
            warnings=warnings,
        )

    def to_standard_schema(self, raw: dict) -> list[KalkiRecord]:
        """
        Transform validated raw data into KalkiRecord instances.

        One KalkiRecord per district per day. Each record:
        - Has a KalkiLocation with state and district
        - Has a data dict with the domain-specific payload
        - Has a data_quality_score between 0.0 and 1.0
        - Has a raw_source_hash for audit trail
        """
        # Compute a hash of the raw source for provenance
        raw_bytes = json.dumps(raw, sort_keys=True).encode()
        source_hash = hashlib.sha256(raw_bytes).hexdigest()

        fetch_time = datetime.now(tz=timezone.utc)
        records = []

        for entry in raw.get("records", []):
            try:
                record_time = datetime.fromisoformat(
                    entry["date"]
                ).replace(tzinfo=timezone.utc)
            except (KeyError, ValueError) as exc:
                logger.warning("Skipping record with bad date: %s — %s", entry, exc)
                continue

            location = KalkiLocation(
                state=entry["state"],
                district=entry["district"],
                state_code=entry.get("state_code"),
                district_lgd_code=entry.get("district_lgd_code"),
            )

            data_payload = {
                "rainfall_mm": entry.get("rainfall_mm"),
                "temperature_max_c": entry.get("temperature_max_c"),
                "temperature_min_c": entry.get("temperature_min_c"),
                "humidity_pct": entry.get("humidity_pct"),
            }

            quality_score = self._compute_quality_score(entry)

            records.append(
                KalkiRecord(
                    source_name="Mock Meteorological Department",
                    source_url="https://example.com/weather-api",
                    connector_version=self.VERSION,
                    module=Module.PRAKRITI,
                    location=location,
                    record_timestamp=record_time,
                    fetch_timestamp=fetch_time,
                    data=data_payload,
                    data_quality_score=quality_score,
                    raw_source_hash=source_hash,
                )
            )

        return records

    def _compute_quality_score(self, entry: dict) -> float:
        """
        Compute a composite data quality score (0.0–1.0).

        Weights follow the Kalki data quality framework (see ARCHITECTURE.md):
          Completeness  30%  — fraction of expected fields present
          Timeliness    25%  — how recent the record is (simplified here)
          Consistency   20%  — values within plausible physical ranges
          Accuracy      15%  — cross-validation (not possible in this mock)
          Provenance    10%  — source has a stable, attributable URL

        In a real connector, timeliness and accuracy checks will be more
        sophisticated (e.g. compare against climatological normals).
        """
        expected_fields = {
            "rainfall_mm", "temperature_max_c",
            "temperature_min_c", "humidity_pct",
        }
        present = sum(1 for f in expected_fields if entry.get(f) is not None)
        completeness = (present / len(expected_fields)) * 0.30

        # Timeliness: assume daily data is always fresh in this mock
        timeliness = 1.0 * 0.25

        # Consistency: basic range checks
        consistent = True
        temp_max = entry.get("temperature_max_c")
        temp_min = entry.get("temperature_min_c")
        humidity = entry.get("humidity_pct")
        rainfall = entry.get("rainfall_mm")

        if temp_max is not None and not (0 <= temp_max <= 60):
            consistent = False
        if temp_min is not None and not (-10 <= temp_min <= 50):
            consistent = False
        if humidity is not None and not (0 <= humidity <= 100):
            consistent = False
        if rainfall is not None and rainfall < 0:
            consistent = False
        consistency = (1.0 if consistent else 0.5) * 0.20

        # Accuracy: no cross-validation available in mock
        accuracy = 0.5 * 0.15

        # Provenance: source URL is stable and attributable
        provenance = 1.0 * 0.10

        return round(completeness + timeliness + consistency + accuracy + provenance, 3)


# ---------------------------------------------------------------------------
# Quick test — run this file directly to see sample output
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    connector = ExampleWeatherConnector()

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
    for r in records:
        print(f"  District:  {r.location.district}, {r.location.state}")
        print(f"  Date:      {r.record_timestamp.date()}")
        print(f"  Data:      {r.data}")
        print(f"  Quality:   {r.data_quality_score}")
        print(f"  Hash:      {r.raw_source_hash[:16]}...")
        print()
