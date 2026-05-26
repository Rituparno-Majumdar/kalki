# IMD District Weather Connector

Fetches district-level daily rainfall observations from the **India Meteorological Department (IMD)**.

## Data Source

| Field | Value |
|-------|-------|
| Organisation | India Meteorological Department |
| Base URL | https://mausam.imd.gov.in |
| Data page | https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=D |
| Update frequency | Daily |
| Access method | HTML scrape; rainfall data is extracted from JavaScript objects embedded in the page HTML |

## What Is Fetched

One `KalkiRecord` per district per day with:

| Field | Unit | Notes |
|-------|------|-------|
| `rainfall_mm` | mm | 24-hour observed rainfall |
| `temperature_max_c` | °C | Always `None`: not available at district level from any public IMD endpoint (see caveats) |
| `temperature_min_c` | °C | Always `None`: not available at district level from any public IMD endpoint (see caveats) |
| `humidity_pct` | % | Always `None`: not available at district level from any public IMD endpoint (see caveats) |

**District LGD code** is extracted from the embedded map data (`id` field) and stored in `KalkiLocation.district_lgd_code`. Use this for joins rather than free-text district names.

## Module

`Module.PRAKRITI` (Climate & Disaster)

## How to Run

```bash
PYTHONPATH=. python3 connectors/imd/connector.py
```

Produces district records for the current day.

## Implementation Notes

The rainfall information page at
`rainfallinformation.php?msg=D` embeds district-level data as a JavaScript
array (`"areas": [...]`) inside the page HTML. Each element contains:

- `title`: district name (uppercase)
- `id`: district LGD code
- `balloonText`: HTML snippet with date, actual rainfall, departure from normal

The connector parses this embedded array using bracket counting and
`json.loads()`; no headless browser required.

## Known Caveats

1. **No REST API**: IMD embeds data in JavaScript; if IMD redesigns the page, `validate()` will report a structural break rather than silently returning empty data.
2. **LGD name mismatch**: District names are uppercase and do not always match LGD canonical names. Use `district_lgd_code` for reliable joins.
3. **Temperature / humidity absent**: These fields are `None` for every record. See [Why Temperature and Humidity Are Not Available](#why-temperature-and-humidity-are-not-available) below for the full investigation.
4. **State field**: Resolved via IMD's own district GeoJSON (`india_gj_2024.geojson`, 766 entries). Districts absent from the GeoJSON fall back to `"India"`.

## Why Temperature and Humidity Are Not Available

This was investigated thoroughly before marking the fields `None`. IMD does not publish district-level temperature or humidity as structured public data. Here is what was found:

| Source | URL | Level | Temp/RH | Notes |
|--------|-----|-------|---------|-------|
| Rainfall page (this connector) | `rainfallinformation.php?msg=D` | District (714) | ✗ | Only rainfall + departure from normal |
| AWS data layer (GeoServer WFS) | `reactjs.imd.gov.in/geoserver/imd/wfs` | **Station** (1 066 today) | ✓ `temp_max`, `temp_min`, `rh` | Station-level only; no district field |
| METAR data layer (GeoServer WFS) | same GeoServer | **Airport station** (145) | ✓ | Station-level only |
| District warnings WFS | `imd:district_warnings_india` | District (764) | ✗ | Warning categories only; no measurements |
| `wxRealized.php` | mausam.imd.gov.in | National | Images only | Temperature shown as `.gif` maps, not data |

**To add temperature and humidity a future contributor would need to:**
1. Fetch all AWS stations from the GeoServer WFS (`imd:aws_data_layer`).
2. Obtain station coordinates from the GeoJSON geometry field.
3. Perform a spatial join against district boundaries to assign each station to a district.
4. Aggregate `temp_max`, `temp_min`, and `rh` per district (e.g., mean or max-station method).

This is non-trivial additional engineering and was out of scope for the initial connector. A follow-up issue should be opened to track this work.

## Output Schema

```python
KalkiRecord(
    source_name="India Meteorological Department",
    source_url="https://mausam.imd.gov.in/responsive/rainfallinformation.php?msg=D",
    connector_version="0.1.0",
    module=Module.PRAKRITI,
    location=KalkiLocation(
        state="Odisha",          # resolved from IMD GeoJSON; "India" if unmatched
        district="Ganjam",       # title-cased from IMD uppercase
        district_lgd_code="373", # from IMD 'id' field
    ),
    record_timestamp=datetime(2026, 5, 23, tzinfo=timezone.utc),
    fetch_timestamp=<when connector ran>,
    data={
        "rainfall_mm": 42.5,
        "temperature_max_c": None,
        "temperature_min_c": None,
        "humidity_pct": None,
    },
    data_quality_score=0.7,      # completeness capped at 0.25/4 fields present
    raw_source_hash="<sha256 of raw HTML>",
)
```
