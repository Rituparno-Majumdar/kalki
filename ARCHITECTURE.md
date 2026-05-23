# Kalki — Technical Architecture

> **Version:** 0.1.0-draft
> **Last Updated:** 2026-05-23
> **Status:** Living Document — contributions welcome
> **Audience:** Senior developers, system architects, module contributors

---

## Table of Contents

- [1. System Overview](#1-system-overview)
- [2. Architecture Diagram](#2-architecture-diagram)
- [3. Layer-by-Layer Deep Dive](#3-layer-by-layer-deep-dive)
  - [3a. Ingestion & Cleaning Layer](#3a-ingestion--cleaning-layer)
  - [3b. Data Lake](#3b-data-lake)
  - [3c. Ontology Layer](#3c-ontology-layer)
  - [3d. Event Streaming](#3d-event-streaming)
  - [3e. Graph Database + Analytical Store](#3e-graph-database--analytical-store)
  - [3f. Analytics & ML Engine](#3f-analytics--ml-engine)
  - [3g. Alerting Engine](#3g-alerting-engine)
  - [3h. API Gateway](#3h-api-gateway)
  - [3i. Dashboard](#3i-dashboard)
  - [3j. Audit & Provenance Layer](#3j-audit--provenance-layer)
- [4. Technology Stack Recommendations](#4-technology-stack-recommendations)
- [5. Connector Interface Specification](#5-connector-interface-specification)
- [6. Data Flow Example: KalkiPrakriti (MVP)](#6-data-flow-example-kalkiprakriti-mvp)
- [7. Deployment Model](#7-deployment-model)
- [8. Security Considerations](#8-security-considerations)

---

## 1. System Overview

Kalki is a **modular, layered data intelligence platform** built for Indian public interest. It ingests, cleans, links, analyzes, and visualizes India's vast ecosystem of public government data — transforming scattered PDFs, dashboards, and portals into structured, queryable, actionable intelligence.

### Core Design Principles

- **Modular architecture.** Each domain module (KalkiPrakriti, KalkiArtha, KalkiSwastha, etc.) plugs into the same core infrastructure. Modules share ingestion pipelines, storage layers, the ontology system, and the dashboard framework — but own their domain-specific logic, models, and connectors.
- **India-scale by default.** The system is designed from day one to handle India's administrative hierarchy: **28 states, 8 Union Territories, 775+ districts, 7,000+ blocks, 250,000+ gram panchayats.** Every entity, every record, every query is location-aware at the appropriate granularity.
- **Public data only.** Kalki ingests exclusively from publicly accessible government sources. No PII. No restricted databases. No scraped private data. See `ETHICS.md` for the full policy.
- **Open source, community-driven.** Every connector, model, and dashboard is open for contribution, audit, and critique. Transparency is a feature, not a constraint.
- **Self-hostable.** The entire stack can run on a single machine (Docker Compose) or scale to a Kubernetes cluster. No vendor lock-in. Indian data stays in Indian data centers.

### Module Architecture

Each Kalki module follows the same structural pattern:

```
kalki-<module>/
├── connectors/          # Data source connectors (one per source)
│   ├── <source_name>/
│   │   ├── connector.py
│   │   ├── config.yaml
│   │   ├── tests/
│   │   └── README.md
├── models/              # ML/analytics models
├── schemas/             # Domain-specific ontology extensions
├── alerts/              # Alert rule definitions
├── dashboards/          # Dashboard page configurations
└── README.md
```

Modules are independently deployable but share the core platform services.

---

## 2. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        PUBLIC DATA SOURCES                          │
│  data.gov.in · IMD · NDMA · IDSP · NREGASoft · UDISE+ · IUDX      │
│  Bhuvan · CPCB · RBI · AgMarkNet · PFMS · GEM · News APIs          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    INGESTION & CLEANING LAYER                        │
│  Scrapers · API Connectors · PDF Parsers · OCR · Schema Normalizer  │
│  Language Detection · Deduplication · Data Quality Scoring           │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         DATA LAKE (RAW)                              │
│              Versioned raw data with full provenance                 │
└──────────────┬───────────────────────────────────┬───────────────────┘
               │                                   │
               ▼                                   ▼
┌──────────────────────────┐         ┌──────────────────────────────┐
│    ONTOLOGY LAYER        │         │    EVENT STREAMING            │
│  Entity Resolution       │         │    Real-time signal ingestion │
│  Schema Mapping          │         │    (Kafka / Redis Streams)    │
│  India-specific Taxonomy │         └──────────────┬───────────────┘
└──────────┬───────────────┘                        │
           │                                        │
           ▼                                        ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     GRAPH DATABASE + DATA WAREHOUSE                  │
│           Neo4j / Apache AGE (graph)  +  DuckDB (analytical)        │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    ANALYTICS & ML ENGINE                              │
│  Pattern Detection · Anomaly Scoring · Forecasting · Clustering      │
│  Bias Detection · Model Registry · Explainability (SHAP/LIME)        │
└──────────────┬───────────────────────────────────┬───────────────────┘
               │                                   │
               ▼                                   ▼
┌──────────────────────────┐         ┌──────────────────────────────┐
│    ALERTING ENGINE       │         │    API GATEWAY                │
│  Threshold-based alerts  │         │    REST + GraphQL             │
│  SMS · Email · Webhook   │         │    Rate-limited, auth'd       │
└──────────────┬───────────┘         └──────────────┬───────────────┘
               │                                    │
               ▼                                    ▼
┌──────────────────────────────────────────────────────────────────────┐
│                         DASHBOARD                                    │
│   District-level maps · Time series · Drill-down · Comparison view   │
│   India shapefiles (state → district → block → village)              │
└──────────────────────────────┬───────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────────┐
│                      AUDIT & PROVENANCE LAYER                        │
│     Full query logs · Data lineage · Access control · DPDPA trail    │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Layer-by-Layer Deep Dive

### 3a. Ingestion & Cleaning Layer

> **This is the hardest problem in the entire system.**

Indian government data is not designed for machine consumption. It arrives in dozens of formats, languages, schemas, and levels of brokenness. The ingestion layer is where Kalki earns its keep.

#### The Reality of Indian Government Data

| Challenge | Examples |
|---|---|
| **PDFs everywhere** | NCRB crime statistics, RBI bulletins, IDSP disease surveillance — all published as PDFs, often scanned images rather than text |
| **Inconsistent schemas** | Same dataset published with different column names year to year, or state to state |
| **Mixed encodings** | UTF-8, ISO-8859-1, Windows-1252, ISCII — often within the same file |
| **Multiple languages** | Headers in Hindi, data in English, footnotes in regional languages |
| **HTML tables** | Most "dashboards" are server-rendered HTML tables with no API |
| **Scanned documents** | Legacy records exist only as scanned images of printed tables |
| **Broken APIs** | When APIs exist, they are often undocumented, rate-limited aggressively, or return malformed responses |

#### Processing Pipeline

```
Source → Fetch → Detect Format → Parse → Detect Language → Normalize Schema
    → Deduplicate → Quality Score → Validate → Store (Data Lake)
```

#### Key Components

**PDF Parsing:**
- `tabula-py` for text-based PDF tables
- `camelot` for complex table layouts with borders
- `Tesseract OCR` (via `pytesseract`) for scanned documents
- `pdfplumber` as a fallback parser
- Custom post-processing to handle merged cells, multi-line headers, and footnotes

**Language Handling:**
- Detection: `langdetect` or `fastText` language identification
- Transliteration: `indic-transliteration` for Devanagari ↔ Latin
- Translation pipeline for headers and metadata (not data values)
- Unicode normalization (NFC) for all Indic scripts

**Schema Normalization:**
- Each connector maps source-specific fields to the Kalki common ontology
- Mapping definitions stored in `connectors/<source>/schema_map.yaml`
- Handles column renames, unit conversions, date format standardization
- Date formats alone can vary: DD/MM/YYYY, YYYY-MM-DD, DD-Mon-YY, Indian fiscal year (Apr-Mar)

**Data Quality Scoring:**
Every record receives a composite quality score (0.0–1.0) based on:

| Dimension | Weight | Description |
|---|---|---|
| Completeness | 0.30 | Percentage of non-null fields |
| Timeliness | 0.25 | How recent the data is relative to expected update frequency |
| Consistency | 0.20 | Internal consistency checks (totals match sums, valid ranges) |
| Accuracy | 0.15 | Cross-validation against other sources where possible |
| Provenance | 0.10 | Source reliability and transformation chain length |

**Deduplication:**
- Fuzzy matching for entity names: `rapidfuzz` for string similarity
- Location deduplication: "Bengaluru" = "Bangalore" = "बेंगलुरु"
- Temporal deduplication: same record published on different dates
- Configurable similarity thresholds per entity type

#### Standard Connector Interface

Every data source connector implements the `BaseConnector` interface (see [Section 5](#5-connector-interface-specification)). This ensures uniformity across the 50+ data sources Kalki will eventually support.

---

### 3b. Data Lake

The data lake stores **all raw ingested data** with full provenance metadata. Nothing is overwritten — every ingestion creates a new version.

#### Storage Layout

```
data-lake/
├── raw/
│   ├── imd/
│   │   ├── 2026-05-23T06:00:00Z/
│   │   │   ├── data.json
│   │   │   ├── metadata.json      # connector version, fetch params, duration
│   │   │   └── quality_report.json
│   │   └── 2026-05-22T06:00:00Z/
│   │       └── ...
│   ├── ndma/
│   └── ncrb/
├── cleaned/
│   ├── imd/
│   │   └── 2026-05-23T06:00:00Z/
│   │       ├── data.parquet
│   │       ├── schema_mapping.json
│   │       └── transformations.json  # exact transformations applied
│   └── ...
└── failed/
    └── imd/
        └── 2026-05-23T12:00:00Z/
            ├── data.json
            ├── error.json           # what went wrong
            └── metadata.json
```

#### Design Decisions

- **Storage backend:** MinIO (S3-compatible, self-hostable, FOSS). Drop-in replacement with AWS S3 for production.
- **File formats:** Raw data stored as-is (JSON, CSV, HTML snapshots). Cleaned data stored as Parquet for efficient analytical queries.
- **Versioning:** Every ingestion run creates a new timestamped directory. No in-place updates, ever.
- **Provenance metadata:** Every file accompanied by `metadata.json` recording:
  - Connector name and version
  - Fetch parameters
  - Fetch timestamp and duration
  - Source URL at time of fetch
  - MD5/SHA256 hash of raw response
- **Retention:** Aligned with `ETHICS.md` data retention policy. Raw data retained for a configurable period; cleaned data retained indefinitely for reproducibility.
- **Failed ingestions:** Stored separately with error details for debugging and monitoring connector health.

---

### 3c. Ontology Layer

The ontology layer solves one of Kalki's fundamental challenges: **making data from dozens of sources talk to each other.** A weather record from IMD, a crop price from AgMarkNet, and a NREGA employment record must all be linkable by location and time.

#### India Administrative Hierarchy

```
India (Nation)
└── State / Union Territory (28 + 8)
    └── Division (optional, not universal)
        └── District (775+)
            └── Sub-district / Tehsil
                └── Block / Taluka (7,000+)
                    └── Gram Panchayat (250,000+)
                        └── Village / Ward
```

#### Core Entity Types

| Entity | Identifier | Source of Truth |
|---|---|---|
| State | Census 2011 State Code | Census of India |
| District | Census 2011 District Code (LGD Code for current) | Local Government Directory (LGD) |
| Block | LGD Block Code | LGD |
| Gram Panchayat | LGD GP Code | LGD |
| Village | Census 2011 Village Code | Census of India |
| Assembly Constituency | ECI AC Code | Election Commission |
| Parliamentary Constituency | ECI PC Code | Election Commission |
| Pin Code | 6-digit PIN | India Post |

#### Entity Resolution

The same district appears differently across sources:

| Source | Spelling |
|---|---|
| IMD | BANGALORE URBAN |
| NCRB | Bengaluru (Urban) |
| Census | Bangalore Urban |
| NREGA | BENGALURU URBAN |

The ontology layer maintains an **alias table** mapping all known spellings to a canonical entity ID (LGD code). This table is community-maintained and grows with each new connector.

```python
# Example: entity resolution lookup
{
    "canonical_id": "LGD-572",
    "canonical_name": "Bengaluru Urban",
    "state": "Karnataka",
    "aliases": [
        "BANGALORE URBAN",
        "Bengaluru (Urban)",
        "Bangalore Urban",
        "BENGALURU URBAN",
        "बेंगलुरु शहरी",
        "ಬೆಂಗಳೂರು ನಗರ"
    ],
    "census_2011_code": "572",
    "lgd_code": "572",
    "iso_3166_2": "IN-KA"
}
```

#### Temporal Alignment

Different sources update at wildly different frequencies:

| Source | Update Frequency |
|---|---|
| CPCB AQI | Every 15 minutes |
| IMD Weather | Hourly |
| AgMarkNet Prices | Daily |
| NREGA Employment | Daily (updated next morning) |
| RBI Monetary Data | Monthly |
| NCRB Crime Data | Annual (2-3 year delay) |
| Census | Decadal |

The ontology layer provides temporal alignment functions that aggregate or interpolate data to common time windows when cross-domain analysis is needed.

#### Domain Schemas

Each module defines domain-specific schemas extending the common ontology:

```yaml
# schemas/prakriti/weather_observation.yaml
entity: weather_observation
fields:
  location_id:
    type: entity_ref
    entity_type: district
    required: true
  timestamp:
    type: datetime
    timezone: IST
    required: true
  temperature_max_c:
    type: float
    unit: celsius
    range: [-10, 55]
  temperature_min_c:
    type: float
    unit: celsius
    range: [-20, 45]
  rainfall_mm:
    type: float
    unit: millimeters
    range: [0, 1000]
  humidity_pct:
    type: float
    unit: percent
    range: [0, 100]
  source:
    type: string
    required: true
  quality_score:
    type: float
    range: [0, 1]
```

---

### 3d. Event Streaming

For signals that demand near-real-time processing — AQI spikes, weather warnings, commodity price surges, news alerts — Kalki uses an event streaming layer.

#### Event Schema

```json
{
    "event_id": "uuid-v4",
    "source": "cpcb_aqi",
    "timestamp": "2026-05-23T06:30:00+05:30",
    "location": {
        "type": "station",
        "id": "CPCB-DL-001",
        "district_id": "LGD-140",
        "state": "Delhi",
        "lat": 28.6139,
        "lon": 77.2090
    },
    "signal_type": "aqi_reading",
    "payload": {
        "aqi": 312,
        "pm25": 185.4,
        "pm10": 290.1,
        "category": "Very Poor"
    },
    "confidence": 0.95,
    "connector_version": "1.2.0"
}
```

#### Topics

| Topic | Description | Consumers |
|---|---|---|
| `kalki.raw.weather` | IMD weather observations | KalkiPrakriti analytics, data lake writer |
| `kalki.raw.aqi` | CPCB AQI readings | KalkiPrakriti analytics, KalkiSwastha correlator |
| `kalki.raw.prices` | AgMarkNet commodity prices | KalkiArtha analytics |
| `kalki.raw.news` | Structured news signals | All modules (NLP pipeline) |
| `kalki.alerts` | Generated alerts | Alerting engine, dashboard, notification service |
| `kalki.anomalies` | Detected anomalies | Analytics engine, dashboard |

#### Implementation

- **Primary:** Apache Kafka (production deployments). Battle-tested, horizontally scalable, exactly-once semantics.
- **Lightweight:** Redis Streams (development and small deployments). Simpler operations, lower resource footprint.
- Consumer groups per module ensure each module processes events independently.
- Dead letter queues for failed event processing.
- Event retention: 7 days in stream, then archived to data lake.

---

### 3e. Graph Database + Analytical Store

Kalki uses **two complementary storage engines** because intelligence questions fall into two distinct categories:

| Question Type | Example | Best Engine |
|---|---|---|
| **Relationship queries** | "What districts share a flood basin with Patna?" | Graph |
| **Trend queries** | "How has AQI changed in Delhi over 5 years?" | Analytical |
| **Cross-domain** | "Districts with rising unemployment AND falling crop prices" | Both |

#### Graph Database: Apache AGE (on PostgreSQL)

**Why Apache AGE over Neo4j Community:**
- AGE runs as a PostgreSQL extension — no separate database to operate
- No license restrictions (Apache 2.0 vs. Neo4j's GPL with commercial restrictions)
- Leverages PostgreSQL's mature ecosystem (backups, replication, tooling)
- Supports openCypher query language

**Graph Model:**

```
(:State)-[:CONTAINS]->(:District)-[:CONTAINS]->(:Block)-[:CONTAINS]->(:GramPanchayat)
(:District)-[:BORDERS]->(:District)
(:District)-[:IN_RIVER_BASIN]->(:RiverBasin)
(:District)-[:HAS_OBSERVATION]->(:WeatherObs {date, temp, rainfall})
(:District)-[:HAS_METRIC]->(:CrimeRate {year, category, rate})
(:District)-[:HAS_METRIC]->(:HealthIndicator {year, indicator, value})
(:Person)-[:REPRESENTS]->(:Constituency)  # elected representatives (public info only)
```

**Example Query:**
```cypher
-- Find districts bordering a flood-affected district that also have poor health infrastructure
MATCH (flood:District {name: "Patna"})-[:BORDERS]->(neighbor:District)
MATCH (neighbor)-[:HAS_METRIC]->(h:HealthIndicator {indicator: "phc_per_lakh"})
WHERE h.value < 1.0
RETURN neighbor.name, h.value
ORDER BY h.value ASC
```

#### Analytical Store: DuckDB

**Why DuckDB:**
- Embedded (in-process), zero-config — no server to manage
- Reads Parquet files directly from the data lake
- Columnar storage, vectorized execution — extremely fast for analytical queries
- SQL-native, familiar to any developer
- Scales to hundreds of GB on a single machine

**For larger deployments:** ClickHouse as a drop-in upgrade when data volumes exceed single-machine capacity.

**Example Query:**
```sql
-- Monthly average AQI trend for Delhi districts, last 2 years
SELECT
    district_name,
    DATE_TRUNC('month', observation_date) AS month,
    AVG(aqi) AS avg_aqi,
    MAX(aqi) AS max_aqi,
    COUNT(*) AS readings
FROM cleaned.aqi_observations
WHERE state = 'Delhi'
  AND observation_date >= CURRENT_DATE - INTERVAL '2 years'
GROUP BY district_name, month
ORDER BY district_name, month;
```

---

### 3f. Analytics & ML Engine

The analytics layer transforms cleaned, linked data into **actionable intelligence** — risk scores, anomaly alerts, forecasts, and patterns.

#### Core Capabilities

**1. Pattern Detection**

| Technique | Use Case | Library |
|---|---|---|
| DBSCAN | Spatial clustering of incidents/events | `scikit-learn` |
| Isolation Forest | Anomaly detection in time series | `scikit-learn` |
| K-Means | District similarity clustering | `scikit-learn` |
| Change Point Detection | Detecting regime changes in trends | `ruptures` |

**2. Forecasting**

| Model | Use Case | Library |
|---|---|---|
| Prophet | Seasonal trends (crop prices, AQI) | `prophet` |
| ARIMA/SARIMA | Short-term forecasting | `statsmodels` |
| XGBoost | Feature-rich prediction (risk scoring) | `xgboost` |
| LSTM (optional) | Complex temporal patterns | `pytorch` |

**3. Risk Scoring**

Each district receives a composite risk score per domain, computed as a weighted aggregation of relevant indicators:

```python
# Example: KalkiPrakriti flood risk score for a district
flood_risk = weighted_average({
    "historical_flood_frequency": (value, 0.25),
    "current_rainfall_anomaly": (value, 0.20),
    "river_basin_water_level": (value, 0.20),
    "drainage_infrastructure_score": (value, 0.15),
    "upstream_rainfall": (value, 0.10),
    "soil_saturation_index": (value, 0.10),
})
# Output: 0.0 (no risk) to 1.0 (extreme risk)
```

**4. Bias Detection**

Every model output is checked against demographic baselines:
- Does the model disproportionately flag certain regions or communities?
- Are training data gaps causing blind spots?
- Automated fairness metrics computed on every model run
- Results logged and surfaced in model documentation

**5. Explainability**

- **SHAP** (SHapley Additive exPlanations) for feature importance on every prediction
- **LIME** (Local Interpretable Model-agnostic Explanations) for individual prediction explanations
- Every alert and risk score links to an explanation of contributing factors
- No black-box outputs — if it cannot be explained, it should not be published

**6. Model Registry**

- **MLflow** for experiment tracking, model versioning, and deployment
- Every model version includes: training data snapshot, hyperparameters, evaluation metrics, bias audit results
- Rollback capability: revert to any previous model version
- A/B testing support for comparing model versions in production

---

### 3g. Alerting Engine

The alerting engine monitors signals and model outputs to push timely warnings through multiple channels.

#### Alert Lifecycle

```
Signal Detected → Threshold Check → Alert Created → Suppression Check
    → Channel Routing → Delivery → Acknowledgment Tracking
```

#### Alert Levels

| Level | Meaning | Channels | Example |
|---|---|---|---|
| 🟢 **Watch** | Developing situation, monitor closely | Dashboard, Email | AQI trending upward in 3 consecutive readings |
| 🟡 **Warning** | Situation requires attention | Dashboard, Email, SMS | District flood risk score exceeds 0.7 |
| 🔴 **Critical** | Immediate attention needed | All channels + Webhook | AQI exceeds 400, active cyclone landfall predicted |

#### Alert Configuration

```yaml
# alerts/prakriti/aqi_alert.yaml
name: aqi_critical
module: prakriti
signal: aqi_reading
conditions:
  - field: payload.aqi
    operator: ">="
    value: 400
    duration: "30m"       # sustained for 30 minutes
level: critical
channels: [dashboard, email, sms, webhook]
cooldown: "4h"            # don't re-alert for same location within 4 hours
message_template: |
  🔴 CRITICAL: AQI at {location.name} has reached {payload.aqi} ({payload.category}).
  PM2.5: {payload.pm25} µg/m³ | PM10: {payload.pm10} µg/m³
  Sustained for {duration}. Source: {source}
```

#### Alert Suppression

To prevent alert fatigue:
- **Cooldown periods:** per-location, per-signal cooldowns (configurable)
- **Escalation:** if a Watch persists for N hours, auto-escalate to Warning
- **Batching:** aggregate multiple related alerts into a single notification
- **Quiet hours:** configurable per-channel (e.g., no SMS between 22:00–06:00 IST unless Critical)

#### Delivery Channels

| Channel | Provider | Notes |
|---|---|---|
| Dashboard | Built-in | Real-time via WebSocket |
| Email | SMTP / SendGrid | Formatted HTML with charts |
| SMS | Government SMS Gateway / Twilio | For critical alerts; character-limited |
| Webhook | HTTP POST | For integration with Slack, Telegram bots, custom systems |
| WhatsApp | WhatsApp Business API | High reach in India; requires approved templates |

---

### 3h. API Gateway

The API gateway exposes Kalki's data and analytics to external consumers — researchers, journalists, civic tech developers, and government dashboards.

#### Endpoints Structure

```
/api/v1/
├── /data/
│   ├── /districts/{district_id}/observations
│   ├── /states/{state_id}/aggregates
│   └── /search
├── /analytics/
│   ├── /risk-scores/{module}/{district_id}
│   ├── /anomalies
│   └── /forecasts/{module}/{district_id}
├── /alerts/
│   ├── /active
│   ├── /history
│   └── /subscribe
├── /meta/
│   ├── /sources
│   ├── /modules
│   ├── /ontology/districts
│   └── /health
└── /graphql
```

#### Design Decisions

- **REST for simple queries, GraphQL for complex cross-domain queries.** Researchers querying multiple datasets simultaneously benefit from GraphQL's flexibility.
- **Authentication:** API keys for registered users (researchers, organizations, developers). Registration is free but tracked for usage analytics and abuse prevention.
- **Rate limiting:** Tiered by user type:

| Tier | Rate Limit | Description |
|---|---|---|
| Anonymous | 100 req/hour | Public dashboard, basic queries |
| Registered | 1,000 req/hour | Researchers, journalists |
| Partner | 10,000 req/hour | Government agencies, NGOs with MOU |
| Internal | Unlimited | Kalki's own dashboard and services |

- **Documentation:** Auto-generated OpenAPI/Swagger docs at `/api/docs`
- **Versioning:** URL-based versioning (`/api/v1/`, `/api/v2/`). Old versions supported for minimum 12 months after deprecation notice.
- **Response format:** JSON by default, CSV export for tabular data, GeoJSON for spatial queries.

---

### 3i. Dashboard

The dashboard is Kalki's public face — where intelligence becomes visible and actionable.

#### Technical Stack

| Component | Technology | Rationale |
|---|---|---|
| Framework | Next.js + React | SSR for SEO, fast initial load, component ecosystem |
| Maps | Leaflet + React-Leaflet | Lightweight, open-source, excellent tile support |
| Charts | D3.js | Maximum flexibility for custom India-specific visualizations |
| Heavy Viz | Deck.gl (optional) | WebGL-powered for large dataset overlays (heatmaps, point clouds) |
| State Management | Zustand or React Context | Lightweight, minimal boilerplate |
| Styling | Vanilla CSS + CSS Modules | No framework lock-in, maximum control |

#### Core Views

**1. National Overview**
- India choropleth map colored by selected metric
- State-level aggregates with click-to-drill-down
- Module selector: switch between Prakriti, Artha, Swastha, etc.
- Time slider: animate changes over time

**2. District Deep Dive**
- All available metrics for a single district
- Cross-module view: weather + economy + health side by side
- Time series charts for trend analysis
- Neighboring district comparison
- Active alerts for the district

**3. Comparison View**
- Side-by-side comparison of any two districts, states, or time periods
- Radar charts for multi-dimensional comparison
- Exportable comparison reports

**4. Alert Dashboard**
- Active alerts by level, module, and location
- Alert history with resolution tracking
- Alert subscription management

#### Map Data

- **India GeoJSON shapefiles** at four levels of granularity:
  - State boundaries (simplified for national view)
  - District boundaries (primary working level)
  - Block boundaries (for deep drill-down)
  - Village boundaries (where available)
- Sources: Survey of India (simplified), Datameet community GeoJSON, LGD
- All shapefiles version-controlled in the repository

#### Localization

- **Minimum:** Hindi and English
- **Extensible:** i18n framework supporting all 22 scheduled languages
- **Implementation:** `next-intl` or `react-i18next`
- **Right-to-left:** Not required for Indian languages but architecture supports it

#### Mobile Responsiveness

- Mobile-first responsive design (many Indian users access via smartphone)
- Touch-optimized map interactions
- Simplified views for smaller screens
- Progressive Web App (PWA) support for offline access in low-connectivity areas

---

### 3j. Audit & Provenance Layer

Per `ETHICS.md` requirements, every action in Kalki is auditable.

#### Audit Log

```json
{
    "log_id": "uuid-v4",
    "timestamp": "2026-05-23T06:30:00+05:30",
    "action": "query",
    "actor": {
        "type": "api_user",
        "id": "usr-12345",
        "ip": "203.0.113.42"
    },
    "resource": {
        "type": "district_risk_score",
        "module": "prakriti",
        "district_id": "LGD-140"
    },
    "details": {
        "query": "GET /api/v1/analytics/risk-scores/prakriti/LGD-140",
        "response_code": 200,
        "response_time_ms": 145
    }
}
```

#### Requirements

- **Immutable:** Append-only log. No edits, no deletions.
- **Data lineage:** Every analytical output traces back to source data, transformations, and model versions.
- **Query logging:** All API queries logged with actor, timestamp, resource, and response metadata.
- **Access control audit:** All permission changes logged.
- **DPDPA compliance:** Even though Kalki stores no PII, the audit trail demonstrates compliance with India's Digital Personal Data Protection Act, 2023.
- **Retention:** Audit logs retained for minimum 3 years.
- **Storage:** Append-only PostgreSQL table or dedicated log store (Loki / Elasticsearch).

---

## 4. Technology Stack Recommendations

| Layer | Recommended | Alternative | Rationale |
|---|---|---|---|
| **Language (Backend)** | Python 3.11+ | — | Largest Indian developer pool, best data science ecosystem, rapid iteration |
| **Language (Performance)** | Go | Rust | For ingestion workers, streaming consumers — where Python is too slow |
| **Frontend** | Next.js + React | — | SSR for SEO, component ecosystem, excellent DX |
| **Visualization** | Leaflet + D3.js | Deck.gl | Leaflet for maps, D3 for charts; Deck.gl for WebGL-heavy scenes |
| **Graph Database** | Apache AGE (PostgreSQL) | Neo4j Community | AGE is Apache 2.0 licensed, PostgreSQL-native, no commercial restrictions |
| **Analytical DB** | DuckDB | ClickHouse | DuckDB is embedded, zero-config, perfect for single-node; ClickHouse for cluster scale |
| **Data Pipeline** | Apache Airflow | Prefect | Airflow is industry standard with massive community; Prefect is more Pythonic and modern |
| **Streaming** | Apache Kafka | Redis Streams | Kafka for production scale with exactly-once semantics; Redis for simpler dev setups |
| **Object Storage** | MinIO | AWS S3 | MinIO is S3-compatible, self-hostable, FOSS; swap to S3 for cloud deployments |
| **ML Platform** | MLflow | — | Experiment tracking, model registry, deployment — industry standard |
| **CI/CD** | GitHub Actions | — | Standard for open-source; free for public repos |
| **Containerization** | Docker + Compose | Kubernetes | Start with Compose for simplicity; migrate to K8s when scale demands it |
| **Hosting** | AWS Mumbai (ap-south-1) | Yotta / CtrlS | Indian region for latency and data sovereignty; Indian cloud providers as alternatives |
| **Monitoring** | Prometheus + Grafana | — | Industry standard, FOSS, excellent dashboard ecosystem |
| **Logging** | Loki | Elasticsearch | Loki is lightweight and integrates natively with Grafana |

### Python Dependency Management

```
# Core
fastapi           # API gateway
uvicorn           # ASGI server
pydantic          # Data validation and schema enforcement
sqlalchemy        # Database ORM (PostgreSQL + AGE)
duckdb            # Embedded analytical database
httpx             # Async HTTP client for connectors
celery            # Task queue for background ingestion

# Data Processing
pandas            # Data manipulation
polars            # High-performance DataFrames (for large datasets)
pyarrow           # Parquet read/write
tabula-py         # PDF table extraction
camelot-py        # Advanced PDF table extraction
pytesseract       # OCR
pdfplumber        # PDF parsing fallback

# ML & Analytics
scikit-learn      # Clustering, anomaly detection
prophet           # Time series forecasting
xgboost           # Gradient boosting
shap              # Model explainability
mlflow            # Experiment tracking

# Streaming
confluent-kafka   # Kafka client
redis             # Redis Streams client

# Utilities
rapidfuzz         # Fuzzy string matching
langdetect        # Language detection
indic-transliteration  # Indic script handling
```

---

## 5. Connector Interface Specification

Every data source connector implements the following interface. This is the contract that enables any contributor to build a connector without understanding the rest of the system.

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class RawDataset:
    """Container for raw data fetched from a source."""
    source_name: str
    fetch_timestamp: datetime
    raw_data: Any                   # bytes, str, dict — whatever the source returns
    raw_format: str                 # "json", "csv", "html", "pdf", "image"
    source_url: str                 # exact URL fetched
    response_headers: dict          # HTTP headers (if applicable)
    fetch_duration_ms: int          # how long the fetch took
    checksum: str                   # SHA256 of raw_data


@dataclass
class CleanDataset:
    """Container for cleaned, normalized data."""
    source_name: str
    fetch_timestamp: datetime
    records: list[dict]             # list of normalized records
    schema_version: str             # version of the schema mapping used
    record_count: int
    transformations: list[str]      # ordered list of transformations applied


@dataclass
class QualityReport:
    """Data quality assessment for a cleaned dataset."""
    overall_score: float            # 0.0 to 1.0
    completeness: float
    timeliness: float
    consistency: float
    accuracy: float
    provenance: float
    issues: list[str]               # human-readable quality issues
    record_count: int
    null_percentage: float


@dataclass
class ValidationResult:
    """Result of data validation checks."""
    is_valid: bool
    errors: list[str]               # blocking errors
    warnings: list[str]             # non-blocking warnings
    records_passed: int
    records_failed: int


class BaseConnector(ABC):
    """Base class for all Kalki data connectors.

    Every connector must implement this interface. Connectors are the bridge
    between the messy reality of Indian government data and Kalki's clean
    internal representation.

    Directory structure for a connector:
        connectors/<source_name>/
        ├── connector.py          # implements BaseConnector
        ├── config.yaml           # source-specific configuration
        ├── schema_map.yaml       # field mapping to Kalki ontology
        ├── tests/
        │   ├── test_fetch.py
        │   ├── test_clean.py
        │   └── fixtures/         # sample data for testing
        ├── QUIRKS.md             # known issues, workarounds, edge cases
        └── README.md             # connector documentation
    """

    @property
    @abstractmethod
    def source_name(self) -> str:
        """Unique identifier for this data source. Example: 'imd_weather'"""
        ...

    @property
    @abstractmethod
    def source_url(self) -> str:
        """Base URL of the data source. Example: 'https://mausam.imd.gov.in'"""
        ...

    @property
    @abstractmethod
    def update_frequency(self) -> str:
        """Expected update frequency. One of: 'realtime', 'hourly', 'daily',
        'weekly', 'monthly', 'quarterly', 'annual'"""
        ...

    @property
    @abstractmethod
    def modules(self) -> list[str]:
        """List of Kalki modules that consume this connector's data.
        Example: ['prakriti', 'swastha']"""
        ...

    @abstractmethod
    def fetch(self, params: dict) -> RawDataset:
        """Fetch raw data from the source.

        Args:
            params: Source-specific fetch parameters (date range, location, etc.)

        Returns:
            RawDataset containing the raw response from the source.

        Raises:
            ConnectorFetchError: If the source is unreachable or returns an error.
            ConnectorRateLimitError: If the source rate-limits the request.
        """
        ...

    @abstractmethod
    def clean(self, raw: RawDataset) -> CleanDataset:
        """Clean and normalize raw data into Kalki's internal schema.

        This is where the hard work happens: parsing PDFs, normalizing
        column names, converting date formats, resolving location names,
        handling missing data, etc.

        Args:
            raw: RawDataset from the fetch step.

        Returns:
            CleanDataset with normalized records.

        Raises:
            ConnectorCleanError: If the data cannot be parsed.
        """
        ...

    @abstractmethod
    def quality_score(self, data: CleanDataset) -> QualityReport:
        """Assess the quality of cleaned data.

        Computes completeness, timeliness, consistency, accuracy, and
        provenance scores. See ARCHITECTURE.md Section 3a for scoring
        methodology.

        Args:
            data: CleanDataset to assess.

        Returns:
            QualityReport with dimensional scores and overall composite.
        """
        ...

    @abstractmethod
    def validate(self, data: CleanDataset) -> ValidationResult:
        """Validate cleaned data against schema and business rules.

        Checks: required fields present, values in valid ranges, referential
        integrity (location IDs exist in ontology), temporal consistency.

        Args:
            data: CleanDataset to validate.

        Returns:
            ValidationResult indicating pass/fail with details.
        """
        ...
```

### Connector Development Checklist

- [ ] Implements `BaseConnector` interface fully
- [ ] `config.yaml` documents all configuration options
- [ ] `schema_map.yaml` maps source fields to Kalki ontology
- [ ] `QUIRKS.md` documents known issues, failure modes, and workarounds
- [ ] Test suite with fixtures covering happy path, edge cases, and failure modes
- [ ] Handles rate limiting gracefully (exponential backoff)
- [ ] Handles source downtime gracefully (retries, cached last-known-good)
- [ ] Logs at appropriate levels (INFO for normal operation, WARNING for degraded, ERROR for failures)
- [ ] README.md documents the source, its quirks, and how to run the connector

---

## 6. Data Flow Example: KalkiPrakriti (MVP)

This section traces a complete data flow through the system for the MVP module: **KalkiPrakriti** (Climate & Disaster Intelligence).

```
┌────────────────────────────────────────────────────────────────┐
│                     DATA SOURCES                                │
│                                                                 │
│  ┌─────────┐  ┌──────────┐  ┌─────────┐  ┌─────────────────┐  │
│  │  IMD    │  │  NDMA    │  │  CPCB   │  │  Bhuvan (ISRO)  │  │
│  │ Weather │  │ Disaster │  │  AQI    │  │  Satellite      │  │
│  └────┬────┘  └────┬─────┘  └────┬────┘  └───────┬─────────┘  │
│       │            │             │                │             │
└───────┼────────────┼─────────────┼────────────────┼─────────────┘
        │            │             │                │
        ▼            ▼             ▼                ▼
┌────────────────────────────────────────────────────────────────┐
│               CONNECTORS (Airflow DAGs)                        │
│                                                                 │
│  connectors/imd/     → fetch hourly weather data               │
│  connectors/ndma/    → scrape disaster history (daily)         │
│  connectors/cpcb/    → poll AQI API (every 15 min)            │
│  connectors/bhuvan/  → download satellite imagery (daily)      │
│                                                                 │
│  Each: fetch → clean → quality_score → validate                │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                    DATA LAKE (MinIO)                            │
│                                                                 │
│  raw/imd/2026-05-23T06:00Z/data.json                          │
│  cleaned/imd/2026-05-23T06:00Z/data.parquet                   │
│  raw/cpcb/2026-05-23T06:15Z/data.json                         │
│  cleaned/cpcb/2026-05-23T06:15Z/data.parquet                  │
└────────────────────────────┬───────────────────────────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────┐
│                 ONTOLOGY RESOLUTION                             │
│                                                                 │
│  "BANGALORE URBAN" → LGD-572 (Bengaluru Urban, Karnataka)     │
│  "NEW DELHI"       → LGD-140 (New Delhi, Delhi)               │
│  Map all records to canonical district IDs                      │
└────────────────────────────┬───────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
┌──────────────────────┐  ┌──────────────────────────────────┐
│   GRAPH DB (AGE)     │  │   ANALYTICAL DB (DuckDB)         │
│                      │  │                                    │
│  District→RiverBasin │  │  Time-series weather observations │
│  District→Borders    │  │  AQI readings by station/district │
│  District→HasAlert   │  │  Historical disaster records      │
└──────────┬───────────┘  └──────────────┬───────────────────┘
           │                             │
           └──────────┬──────────────────┘
                      ▼
┌────────────────────────────────────────────────────────────────┐
│                  ANALYTICS ENGINE                               │
│                                                                 │
│  1. Compute district-level risk scores:                        │
│     - Flood risk (rainfall + river basin + historical)         │
│     - Drought risk (rainfall deficit + soil moisture)          │
│     - Cyclone risk (coastal proximity + IMD warnings)          │
│     - Heatwave risk (temperature anomaly + duration)           │
│                                                                 │
│  2. Anomaly detection:                                         │
│     - Unusual AQI spikes                                       │
│     - Rainfall significantly above/below normal                │
│                                                                 │
│  3. Forecasting:                                               │
│     - 7-day rainfall forecast (Prophet)                        │
│     - AQI trend prediction                                     │
└────────────────────────────┬───────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
┌──────────────────────┐  ┌──────────────────────────────────┐
│   ALERTING ENGINE    │  │   DASHBOARD                      │
│                      │  │                                    │
│  AQI > 400 → 🔴     │  │  India map: flood risk by district│
│  Flood risk > 0.7 →  │  │  Time series: AQI trends         │
│    🟡 Warning        │  │  Drill-down: district detail      │
│  Send SMS, Email     │  │  Comparison: district vs district │
└──────────────────────┘  └──────────────────────────────────┘
```

### Airflow DAG Example

```python
# dags/prakriti_imd_weather.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "kalki-prakriti",
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="prakriti_imd_weather_ingest",
    default_args=default_args,
    schedule_interval="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["prakriti", "imd", "weather"],
) as dag:

    fetch = PythonOperator(
        task_id="fetch_imd_weather",
        python_callable=imd_connector.fetch,
        op_kwargs={"params": {"date": "{{ ds }}"}},
    )

    clean = PythonOperator(
        task_id="clean_imd_weather",
        python_callable=imd_connector.clean,
    )

    score = PythonOperator(
        task_id="quality_score",
        python_callable=imd_connector.quality_score,
    )

    validate = PythonOperator(
        task_id="validate",
        python_callable=imd_connector.validate,
    )

    store = PythonOperator(
        task_id="store_to_datalake",
        python_callable=datalake.store,
    )

    resolve = PythonOperator(
        task_id="ontology_resolve",
        python_callable=ontology.resolve_locations,
    )

    load_graph = PythonOperator(
        task_id="load_graph_db",
        python_callable=graph_loader.load,
    )

    load_analytical = PythonOperator(
        task_id="load_analytical_db",
        python_callable=analytical_loader.load,
    )

    fetch >> clean >> score >> validate >> store >> resolve >> [load_graph, load_analytical]
```

---

## 7. Deployment Model

### Development (Single Developer)

```yaml
# docker-compose.dev.yml
services:
  postgres:        # PostgreSQL + Apache AGE
  minio:           # Object storage (data lake)
  redis:           # Caching + lightweight streaming
  airflow:         # Pipeline orchestration
  api:             # FastAPI backend
  dashboard:       # Next.js frontend
  mlflow:          # ML experiment tracking
```

Single command: `docker compose -f docker-compose.dev.yml up`

### Staging (Single VM)

- Same Docker Compose stack on a dedicated VM
- Adds: Prometheus + Grafana for monitoring
- Adds: Nginx reverse proxy with SSL
- Minimum specs: 4 vCPU, 16 GB RAM, 500 GB SSD

### Production (Scalable)

- **Orchestration:** Kubernetes (or Docker Swarm for smaller scale)
- **Database:** Managed PostgreSQL (with AGE extension) or self-hosted with replication
- **Storage:** MinIO cluster or AWS S3 (ap-south-1)
- **Streaming:** Managed Kafka or self-hosted Kafka cluster
- **CDN:** CloudFront or equivalent for dashboard static assets
- **Monitoring:** Prometheus + Grafana + Loki + AlertManager

### Data Sovereignty

> **All data must be stored in Indian data centers.**

- AWS: `ap-south-1` (Mumbai) or `ap-south-2` (Hyderabad)
- Indian cloud: Yotta (Navi Mumbai), CtrlS (Hyderabad), NxtGen (Bangalore)
- Self-hosted: Indian colocation facilities
- No data replication to non-Indian regions

### Redundancy

- **Database:** Primary-replica PostgreSQL with automated failover
- **Object storage:** MinIO erasure coding or S3 cross-AZ replication
- **Application:** Multiple replicas behind load balancer
- **Backups:** Daily automated backups with 30-day retention
- **Disaster recovery:** RTO < 4 hours, RPO < 1 hour

---

## 8. Security Considerations

### Principles

1. **No PII by design.** Kalki processes only aggregate public data. No individual names, addresses, Aadhaar numbers, or other personal identifiers are stored. If a data source contains PII, the connector must strip it during the clean step.

2. **Defense in depth.** Multiple layers of security, not reliance on any single mechanism.

### Implementation

| Area | Measure |
|---|---|
| **Transport** | HTTPS everywhere. TLS 1.2+ enforced. HSTS headers on all endpoints. |
| **Authentication** | API keys for all write operations and elevated-rate queries. OAuth 2.0 for admin dashboard access. |
| **Authorization** | Role-based access control (RBAC): public reader, registered user, module admin, platform admin. |
| **Dashboard** | Read-only public access for all data views. Authenticated admin access for configuration and alert management. |
| **Secrets** | All credentials in environment variables or a secrets manager (HashiCorp Vault / AWS Secrets Manager). Never in code or config files. |
| **Dependencies** | Automated scanning with Dependabot (GitHub) and Snyk. Weekly vulnerability reports. |
| **Containers** | Minimal base images (Alpine/distroless). No root processes. Read-only filesystems where possible. |
| **Network** | Internal services on private network. Only API gateway and dashboard exposed publicly. |
| **Rate limiting** | Tiered rate limits on all public endpoints (see Section 3h). IP-based throttling for unauthenticated requests. |
| **Input validation** | All API inputs validated with Pydantic models. SQL injection prevention via parameterized queries. XSS prevention in dashboard. |
| **Logging** | Security events logged to immutable audit trail (see Section 3j). Failed authentication attempts tracked and alerted. |
| **Incident response** | Documented incident response plan. Security contact in README. Responsible disclosure policy. |

### Dependency Policy

- Pin all dependency versions in lockfiles
- Automated PR for dependency updates (Dependabot)
- No dependencies with known critical CVEs in production
- Prefer well-maintained, widely-used libraries
- Audit new dependencies before adoption (license, maintenance status, security history)

---

> **Next Steps:**
> - Read `DATA_SOURCES.md` for the complete data source registry
> - Read `ETHICS.md` for the ethical framework and constraints
> - Read `CONTRIBUTING.md` for how to build your first connector
> - Read `README.md` for the project overview and quick start

---

*This is a living document. If you see something missing or wrong, open an issue or submit a PR.*
