"""
IMD Connector — comprehensive unit test suite (55 tests).

Run from repo root:
    python -m pytest tests/connectors/test_imd_connector.py -v
"""

from __future__ import annotations

import hashlib

import pytest

from connectors.imd.connector import (
    IMDConnector,
    _extract_areas,
    _parse_balloon,
    _safe_float,
)
from schema.models import Module


# ---------------------------------------------------------------------------
# Fixtures / shared constants
# ---------------------------------------------------------------------------

FIXTURE_HTML = (
    b'"areas": ['
    b'{"title":"GANJAM","id":"373","balloonText":"Date : 2026-05-23 Actual : 42.5 mm"},'
    b'{"title":"PURI","id":"374","balloonText":"Date : 2026-05-23 Actual : 0.0 mm"},'
    b'{"title":"KHURDA","id":"375","balloonText":"Date : 2026-05-23 Actual : 8.2 mm"}'
    b'] "balloonText": "Actual" mm'
)

FIXTURE_STATE_MAP = {
    "GANJAM": "Odisha",
    "PURI": "Odisha",
}

MINIMAL_RAW = {
    "html": (
        b'"areas": [{"title":"GANJAM","id":"373",'
        b'"balloonText":"Date : 2026-05-23 Actual : 42.5 mm"}]'
        b' "balloonText": "Actual" mm'
    ),
    "state_map": {"GANJAM": "Odisha"},
}


# ---------------------------------------------------------------------------
# _safe_float: 8 tests
# Maintainer required: NaN, None, non-numeric values
# ---------------------------------------------------------------------------

class TestSafeFloat:
    def test_integer_string(self):
        assert _safe_float("42") == 42.0

    def test_float_string(self):
        assert _safe_float("3.14") == 3.14

    def test_zero_string(self):
        assert _safe_float("0") == 0.0

    def test_nan_string_returns_none(self):
        assert _safe_float("NaN") is None

    def test_nan_float_returns_none(self):
        assert _safe_float(float("nan")) is None

    def test_empty_string_returns_none(self):
        assert _safe_float("") is None

    def test_none_input_returns_none(self):
        assert _safe_float(None) is None

    def test_non_numeric_string_returns_none(self):
        assert _safe_float("abc") is None


# ---------------------------------------------------------------------------
# _parse_balloon: 5 tests
# Maintainer required: date and rainfall patterns
# ---------------------------------------------------------------------------

class TestParseBalloon:
    BALLOON = "<b>Date : 2026-05-23</b><br>Actual : 42.5 mm<br>Departure : +5.0 mm"

    def test_parse_date(self):
        assert _parse_balloon(self.BALLOON, r"Date\s*:\s*([\d-]+)") == "2026-05-23"

    def test_parse_actual_rainfall(self):
        assert _parse_balloon(self.BALLOON, r"Actual\s*:\s*([\d.]+)\s*mm") == "42.5"

    def test_no_match_returns_none(self):
        assert _parse_balloon(self.BALLOON, r"Temperature\s*:\s*([\d.]+)") is None

    def test_empty_balloon_returns_none(self):
        assert _parse_balloon("", r"Date\s*:\s*([\d-]+)") is None

    def test_zero_rainfall(self):
        b = "<b>Date : 2026-05-23</b><br>Actual : 0.0 mm"
        assert _parse_balloon(b, r"Actual\s*:\s*([\d.]+)\s*mm") == "0.0"


# ---------------------------------------------------------------------------
# _extract_areas: 5 tests
# Maintainer required: valid HTML, missing marker, malformed JSON
# ---------------------------------------------------------------------------

SAMPLE_AREAS = (
    '"areas": [{"title":"GANJAM","id":"373",'
    '"balloonText":"<b>Date : 2026-05-23</b><br>Actual : 42.5 mm"},'
    '{"title":"PURI","id":"374",'
    '"balloonText":"<b>Date : 2026-05-23</b><br>Actual : 0.0 mm"}]'
)


class TestExtractAreas:
    def test_parses_correct_count(self):
        assert len(_extract_areas(SAMPLE_AREAS)) == 2

    def test_first_district_title(self):
        assert _extract_areas(SAMPLE_AREAS)[0]["title"] == "GANJAM"

    def test_empty_array_returns_empty_list(self):
        assert _extract_areas('"areas": []') == []

    def test_missing_marker_returns_empty(self):
        assert _extract_areas("no areas marker here") == []

    def test_malformed_json_returns_empty(self):
        assert _extract_areas('"areas": [{broken json}]') == []


# ---------------------------------------------------------------------------
# validate(): 7 tests
# Maintainer required: happy path and structural-break cases
# ---------------------------------------------------------------------------

VALID_HTML = (
    b'"areas": [{"title":"DIST","id":"1",'
    b'"balloonText":"Date : 2026-05-23 Actual : 5 mm"}]'
    b' "balloonText": "Actual" mm'
)


class TestValidate:
    def setup_method(self):
        self.connector = IMDConnector()

    def test_valid_html_passes(self):
        result = self.connector.validate({"html": VALID_HTML, "state_map": {"DIST": "State"}})
        assert result.is_valid

    def test_empty_html_is_invalid(self):
        result = self.connector.validate({"html": b"", "state_map": {}})
        assert not result.is_valid
        assert any("Empty" in i for i in result.issues)

    def test_missing_areas_key_is_invalid(self):
        result = self.connector.validate({"html": b"<html>no marker</html>", "state_map": {}})
        assert not result.is_valid
        assert any("areas" in i for i in result.issues)

    def test_missing_balloontext_key_is_invalid(self):
        html = b'"areas": [] no balloon'
        result = self.connector.validate({"html": html, "state_map": {}})
        assert not result.is_valid
        assert any("balloonText" in i for i in result.issues)

    def test_empty_state_map_gives_warning_but_valid(self):
        result = self.connector.validate({"html": VALID_HTML, "state_map": {}})
        assert result.is_valid
        assert len(result.warnings) > 0

    def test_no_rainfall_values_gives_warning_but_valid(self):
        html = b'"areas": [] "balloonText": [] some content without rainfall'
        result = self.connector.validate({"html": html, "state_map": {"X": "Y"}})
        assert result.is_valid
        assert len(result.warnings) > 0

    def test_valid_result_has_no_blocking_issues(self):
        result = self.connector.validate({"html": VALID_HTML, "state_map": {"DIST": "State"}})
        assert result.issues == []


# ---------------------------------------------------------------------------
# to_standard_schema(): 16 tests
# Maintainer required: fixture HTML blob end-to-end
# ---------------------------------------------------------------------------

class TestToStandardSchema:
    def setup_method(self):
        self.connector = IMDConnector()

    def _run(self, raw=None):
        return self.connector.to_standard_schema(raw or MINIMAL_RAW)

    def test_one_record_per_district(self):
        raw = {"html": FIXTURE_HTML, "state_map": FIXTURE_STATE_MAP}
        assert len(self.connector.to_standard_schema(raw)) == 3

    def test_district_is_title_cased(self):
        assert self._run()[0].location.district == "Ganjam"

    def test_state_resolved_from_map(self):
        assert self._run()[0].location.state == "Odisha"

    def test_state_falls_back_to_india_when_not_in_map(self):
        raw = {"html": FIXTURE_HTML, "state_map": FIXTURE_STATE_MAP}
        records = self.connector.to_standard_schema(raw)
        khurda = next(r for r in records if r.location.district == "Khurda")
        assert khurda.location.state == "India"

    def test_state_falls_back_to_india_when_map_empty(self):
        raw = dict(MINIMAL_RAW, state_map={})
        assert self._run(raw)[0].location.state == "India"

    def test_lgd_code_populated(self):
        assert self._run()[0].location.district_lgd_code == "373"

    def test_rainfall_value_correct(self):
        assert self._run()[0].data["rainfall_mm"] == 42.5

    def test_zero_rainfall_included(self):
        raw = {"html": FIXTURE_HTML, "state_map": FIXTURE_STATE_MAP}
        records = self.connector.to_standard_schema(raw)
        puri = next(r for r in records if r.location.district == "Puri")
        assert puri.data["rainfall_mm"] == 0.0

    def test_temperature_max_is_none(self):
        assert self._run()[0].data["temperature_max_c"] is None

    def test_humidity_is_none(self):
        assert self._run()[0].data["humidity_pct"] is None

    def test_record_timestamp_matches_balloon_date(self):
        assert self._run()[0].record_timestamp.date().isoformat() == "2026-05-23"

    def test_raw_source_hash_is_sha256_of_html(self):
        expected = hashlib.sha256(MINIMAL_RAW["html"]).hexdigest()
        assert self._run()[0].raw_source_hash == expected

    def test_skips_district_with_no_date(self):
        raw = {
            "html": b'"areas": [{"title":"X","id":"1","balloonText":"Actual : 5 mm"}]'
                    b' "balloonText": "Actual" mm',
            "state_map": {},
        }
        assert self._run(raw) == []

    def test_skips_district_with_no_rainfall(self):
        raw = {
            "html": b'"areas": [{"title":"X","id":"1","balloonText":"Date : 2026-05-23"}]'
                    b' "balloonText": "Actual" mm',
            "state_map": {},
        }
        assert self._run(raw) == []

    def test_empty_areas_returns_empty_list(self):
        raw = {
            "html": b'"areas": [] "balloonText": "Actual" mm',
            "state_map": {},
        }
        assert self._run(raw) == []

    def test_module_is_prakriti(self):
        assert self._run()[0].module == Module.PRAKRITI


# ---------------------------------------------------------------------------
# _compute_quality_score: 6 tests
# Maintainer required: only rainfall vs. all fields present
# ---------------------------------------------------------------------------

class TestComputeQualityScore:
    def _score(self, **overrides):
        base = {
            "rainfall_mm": 10.0,
            "temperature_max_c": None,
            "temperature_min_c": None,
            "humidity_pct": None,
        }
        base.update(overrides)
        return IMDConnector._compute_quality_score(base)

    def test_only_rainfall_gives_0_700(self):
        # completeness=0.075 timeliness=0.25 consistency=0.20 accuracy=0.075 provenance=0.10
        assert self._score() == pytest.approx(0.700, abs=0.001)

    def test_all_fields_present_score_above_0_9(self):
        full = self._score(temperature_max_c=35.0, temperature_min_c=22.0, humidity_pct=75.0)
        assert full > 0.9

    def test_negative_rainfall_reduces_consistency(self):
        assert self._score(rainfall_mm=-5.0) < self._score(rainfall_mm=5.0)

    def test_out_of_range_temp_reduces_consistency(self):
        full_valid = self._score(temperature_max_c=35.0, temperature_min_c=22.0, humidity_pct=75.0)
        full_bad = self._score(temperature_max_c=999.0, temperature_min_c=22.0, humidity_pct=75.0)
        assert full_bad < full_valid

    def test_is_a_static_method(self):
        result = IMDConnector._compute_quality_score({
            "rainfall_mm": 5.0,
            "temperature_max_c": None,
            "temperature_min_c": None,
            "humidity_pct": None,
        })
        assert isinstance(result, float)

    def test_score_rounded_to_3_decimal_places(self):
        s = self._score()
        assert round(s, 3) == s


# ---------------------------------------------------------------------------
# BaseConnector contract: 8 tests
# ---------------------------------------------------------------------------

class TestBaseConnectorContract:
    def setup_method(self):
        self.connector = IMDConnector()

    def test_has_get_metadata(self):
        assert callable(getattr(self.connector, "get_metadata", None))

    def test_has_fetch(self):
        assert callable(getattr(self.connector, "fetch", None))

    def test_has_validate(self):
        assert callable(getattr(self.connector, "validate", None))

    def test_has_to_standard_schema(self):
        assert callable(getattr(self.connector, "to_standard_schema", None))

    def test_has_run(self):
        assert callable(getattr(self.connector, "run", None))

    def test_metadata_module_is_prakriti(self):
        assert self.connector.get_metadata().module == Module.PRAKRITI

    def test_metadata_version_is_semver(self):
        v = self.connector.get_metadata().version
        parts = v.split(".")
        assert len(parts) == 3 and all(p.isdigit() for p in parts)

    def test_metadata_maintainer_set(self):
        assert self.connector.get_metadata().maintainer == "suiiibhit"
