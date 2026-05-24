# Kalki Connectors

A **connector** is a Python class that fetches, validates, and normalises
data from a single Indian government data source into the standard Kalki
schema. One connector = one source.

---

## Quick Start

```bash
# Run the example connector (no network calls, no setup required)
# Run from the repo root:
PYTHONPATH=. python3 connectors/example_connector.py
```

---

## How to Build a Connector

### 1. Pick a data source

Browse the open issues labelled `[Connector]` on GitHub. Each issue
specifies the source URL, expected output, and acceptance criteria.

If you want to add a source that isn't in the issues list, open an issue
first so maintainers can confirm it meets the public-data-only requirement.

### 2. Create your connector directory

```
connectors/
└── your_source_name/
    ├── __init__.py
    ├── connector.py     ← your implementation goes here
    └── README.md        ← describe the source, caveats, and test instructions
```

### 3. Implement BaseConnector

```python
from connectors.base_connector import BaseConnector, ConnectorMetadata, ...

class YourSourceConnector(BaseConnector):
    def get_metadata(self) -> ConnectorMetadata: ...
    def fetch(self) -> Any: ...
    def validate(self, raw: Any) -> ValidationResult: ...
    def to_standard_schema(self, raw: Any) -> list[KalkiRecord]: ...
```

See `example_connector.py` for a fully-annotated walkthrough of every method.

### 4. Run it locally

```bash
# From the repo root:
PYTHONPATH=. python3 connectors/your_source_name/connector.py
```

### 5. Open a PR

Follow the checklist in `CONTRIBUTING.md`. A maintainer will review against
the connector acceptance criteria.

---

## Connector Acceptance Criteria

A connector PR will be merged when it:

- [ ] Inherits from `BaseConnector` and implements all four methods
- [ ] Returns `list[KalkiRecord]` from `to_standard_schema()`
- [ ] Computes `data_quality_score` for every record
- [ ] Stores `raw_source_hash` (SHA-256 of raw source) on every record
- [ ] Uses only publicly accessible data (no private API keys required)
- [ ] Includes a `connectors/your_source/README.md` with source description and caveats
- [ ] Passes `python connectors/your_source/connector.py` without errors

---

## Files in This Directory

| File | Purpose |
|---|---|
| `base_connector.py` | Abstract base class — the contract every connector must fulfil |
| `example_connector.py` | Fully-annotated reference implementation using mock data |
| `imd/` | India Meteorological Department — daily district rainfall |
| `ndma/` | National Disaster Management Authority *(open issue)* |
| `cpcb/` | Central Pollution Control Board *(open issue)* |
