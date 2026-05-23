<p align="center">
  <img src="docs/assets/kalki-logo-placeholder.png" alt="Kalki Logo" width="200"/>
</p>

<h1 align="center">Kalki</h1>
<h3 align="center">India's Open Intelligence Platform</h3>

<p align="center">
  <em>Surfacing early signals from public data — so India can see what's coming.</em>
</p>

<p align="center">
  <a href="#modules">Modules</a> •
  <a href="#architecture">Architecture</a> •
  <a href="#get-started">Get Started</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="ETHICS.md">Ethics</a> •
  <a href="GOVERNANCE.md">Governance</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-AGPL--3.0-blue.svg" alt="License: AGPL-3.0"/>
  <img src="https://img.shields.io/badge/MVP-KalkiPrakriti-green.svg" alt="MVP: KalkiPrakriti"/>
  <img src="https://img.shields.io/badge/data-public%20only-brightgreen.svg" alt="Public Data Only"/>
  <img src="https://img.shields.io/badge/PRs-welcome-orange.svg" alt="PRs Welcome"/>
</p>

---

> **यदा यदा हि धर्मस्य ग्लानिर्भवति भारत ।**
> **अभ्युत्थानमधर्मस्य तदात्मानं सृजाम्यहम् ॥**
>
> *Whenever dharma declines and adharma rises, I manifest myself.*
> — Bhagavad Gita 4.7

---

## What is Kalki?

**Kalki** is an open-source intelligence and forecasting platform built for India, by India.

It ingests publicly available data — from government portals, meteorological services, health surveillance systems, economic indicators, and more — and transforms it into **actionable early-warning signals** that help citizens, researchers, journalists, administrators, and policymakers understand what is likely to happen before a crisis grows.

Kalki is **not** a surveillance system. It is **not** a predictive policing tool. It is **not** an autonomous enforcement engine.

Kalki is a **decision-support system**: it surfaces patterns from public data so that humans can make better decisions. Every output requires human review. Every signal is traceable to its source. Every model is auditable for bias.

Think of it as an open, ethical, India-first alternative to the high-level concept of systems like Palantir Gotham — but designed for public interest, built in the open, and governed by the community.

---

## Why Does This Exist?

India generates enormous amounts of public data across hundreds of government portals, dashboards, and reporting systems. But this data is:

- **Fragmented** — scattered across NCRB, IMD, IDSP, NREGASoft, UDISE+, and dozens of other sources
- **Inconsistent** — different formats (PDFs, Excel, HTML, scanned images), different schemas, different languages
- **Siloed** — crime data doesn't talk to economic data; health data doesn't talk to climate data
- **Delayed** — some datasets are 2-3 years behind
- **Underutilized** — the signals are there, but no one is connecting the dots

Meanwhile, India faces interconnected challenges that don't respect departmental boundaries:

- A drought in Marathwada affects crop yields, which affects farmer income, which affects loan defaults, which affects migration patterns, which affects urban infrastructure strain.
- An air quality collapse in Delhi correlates with respiratory hospital admissions, which correlates with school absenteeism, which reveals infrastructure gaps in health and education simultaneously.

**Kalki exists to connect these dots.** To take fragmented public data, clean it, link it, analyze it, and surface the early signals that help India prepare rather than react.

---

## Core Principles

These are non-negotiable. They are not aspirations — they are constraints.

| Principle | What It Means |
|---|---|
| **Public Data Only** | Kalki will never use private, restricted, or illegally obtained data. Every data source must be publicly accessible or obtainable through RTI. |
| **Privacy-First Design** | No individual profiling. No personal data storage. All outputs are aggregate-level. k-anonymity guarantees: no output for groups smaller than 100 individuals. |
| **Human-in-the-Loop** | Every Kalki output is a signal for human review, never an automated decision. No autonomous enforcement, punishment, or action. |
| **No Surveillance** | Kalki will never perform real-time tracking, facial recognition, social credit scoring, or predictive policing at the individual level. |
| **Bias Auditing** | Every model output is tested against demographic baselines. If a pattern correlates with caste, religion, or gender demographics, it is flagged before publication. |
| **Full Transparency** | All code is open source. All models are explainable. All data lineage is traceable. Audit logs are maintained for all queries. |
| **DPDPA 2023 Compliance** | Kalki operates within the Digital Personal Data Protection Act, 2023. See [ETHICS.md](ETHICS.md) for the full compliance framework. |

> For the complete operational ethics framework, including the Ethics Board charter, bias detection requirements, right-to-contest process, and red lines, see **[ETHICS.md](ETHICS.md)**.

---

## Modules

Kalki is organized into eight domain modules, each focusing on a specific category of public signals. Modules are **independent but interconnected** — they share common infrastructure but can be built, deployed, and maintained separately.

### Build Order

Modules are ordered by **risk level** (low → high) and **data availability** (high → low). We build the safest, most data-rich modules first.

| Priority | Module | Domain | Risk | Data Availability | Status |
|:---:|---|---|:---:|:---:|:---:|
| 1 | [**KalkiPrakriti**](#kalkiprakriti-) 🌿 | Climate & Disaster | 🟢 Low | 🟢 High | **MVP — Active** |
| 2 | [**KalkiShiksha**](#kalkishiksha-) 📚 | Education | 🟢 Low | 🟢 High | Planned |
| 3 | [**KalkiSwastha**](#kalkiswastha-) 🏥 | Health & Epidemiology | 🟢 Low | 🟡 Medium | Planned |
| 4 | [**KalkiArtha**](#kalkiartha-) 💰 | Economic Stress | 🟡 Medium | 🟡 Medium | Planned |
| 5 | [**KalkiNagrik**](#kalkinagrik-) 🏙️ | Civic Infrastructure | 🟢 Low | 🟡 Medium | Planned |
| 6 | [**KalkiSamaj**](#kalkisamaj-) 👥 | Social & Demographic | 🟡 Medium | 🟡 Medium | Planned |
| 7 | [**KalkiDharma**](#kalkidharma-) ⚖️ | Governance & Transparency | 🟠 Medium-High | 🟡 Medium | Planned |
| 8 | [**KalkiCrime**](#kalkicrime-) 🔍 | Crime Patterns | 🔴 High | 🔴 Low | Future |

---

### KalkiPrakriti 🌿
**Climate & Disaster Risk — MVP Module**

The first module to be built. Lowest risk, highest data availability, most universally understood problem.

**Signals:**
- District-level flood, drought, cyclone, and heatwave risk scoring
- Air quality and health correlation mapping
- Disaster preparedness gap analysis
- Seasonal risk forecasting

**Key Data Sources:** IMD, NDMA, CPCB, Bhuvan (ISRO), IUDX, data.gov.in

---

### KalkiShiksha 📚
**Education**

**Signals:**
- School dropout clustering and early warning
- Teacher vacancy and quality mapping
- Infrastructure gaps (toilets, electricity, computers)
- Learning outcome disparities across districts

**Key Data Sources:** UDISE+, NAS (National Achievement Survey), data.gov.in

---

### KalkiSwastha 🏥
**Health & Epidemiology**

**Signals:**
- Disease outbreak early warning
- Hospital capacity mismatch detection
- Air quality and respiratory health correlation
- Vaccination coverage gaps

**Key Data Sources:** IDSP, HMIS, CPCB, CoWIN/eSanjeevani, state health dashboards

---

### KalkiArtha 💰
**Economic Stress Indicators**

**Signals:**
- Unemployment spikes and regional clustering
- Crop failure and farmer distress indicators
- MSP procurement anomalies
- Loan default clustering
- Migration wave prediction

**Key Data Sources:** RBI aggregates, AgMarkNet, PMFBY, MoLE, EPFO, data.gov.in

---

### KalkiNagrik 🏙️
**Civic Infrastructure**

**Signals:**
- Water supply coverage and quality gaps
- Sanitation infrastructure status
- Housing shortage mapping
- Smart city project progress vs. targets

**Key Data Sources:** Jal Jeevan Mission, Swachh Bharat, Smart City dashboards, PMAY

---

### KalkiSamaj 👥
**Social & Demographic**

**Signals:**
- Literacy and dropout correlation mapping
- Child malnutrition zone identification
- Domestic violence cluster mapping
- Missing persons risk zone analysis

**Key Data Sources:** Census of India, NFHS, POSHAN Abhiyaan, NCW

**Ethics Note:** All outputs framed for prevention and support, never for stigmatizing communities.

---

### KalkiDharma ⚖️
**Governance & Transparency**

**Signals:**
- MGNREGA fund leakage pattern detection
- Tender anomaly flagging
- Mid-day meal irregularities
- Ghost beneficiary detection
- Government expenditure tracking anomalies

**Key Data Sources:** NREGASoft, GeM, PFMS, DBT Bharat

**Ethics Note:** Reports anomalies as flags for human review, never as accusations.

---

### KalkiCrime 🔍
**Crime Patterns — Build Last**

**Signals:**
- FIR density heatmaps by district
- Crime type clustering and seasonal patterns
- Cybercrime surge detection
- Communal tension early warning (aggregate, area-level only)

**Key Data Sources:** NCRB (2-3 year delay), CERT-In advisories, data.gov.in

**Ethics Note:** This module carries the highest risk of misuse. It will be built last, with the strictest ethical guardrails:
- District-level minimum aggregation (never locality-level)
- Mandatory demographic bias audits on every output
- Ethics Board reviews every new signal type before deployment
- Read-only analytics only — no real-time tracking

> ⚠️ **Note:** CCTNS and state police databases are **not** used. They are restricted law enforcement systems and violate Kalki's public-data-only principle.

---

## Architecture

Kalki uses a modular, layered architecture designed for India-scale data processing.

```
┌───────────────────────────────────────────────────────────────────────┐
│                        PUBLIC DATA SOURCES                            │
│  data.gov.in · IMD · NDMA · IDSP · NREGASoft · UDISE+ · IUDX        │
│  Bhuvan · CPCB · RBI · AgMarkNet · PFMS · GEM · News APIs            │
└──────────────────────────────┬────────────────────────────────────────┘
                               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    INGESTION & CLEANING LAYER                         │
│  Scrapers · API Connectors · PDF Parsers · OCR · Schema Normalizer   │
│  Language Detection · Deduplication · Data Quality Scoring            │
└──────────────────────────────┬────────────────────────────────────────┘
                               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                          DATA LAKE (RAW)                              │
│               Versioned raw data with full provenance                 │
└──────────────┬───────────────────────────────────┬────────────────────┘
               ▼                                   ▼
┌──────────────────────────┐          ┌─────────────────────────────────┐
│    ONTOLOGY LAYER        │          │     EVENT STREAMING             │
│  Entity Resolution       │          │     Real-time signal ingestion  │
│  Schema Mapping          │          │     (Kafka / Pulsar)            │
│  India-specific Taxonomy │          └──────────────┬──────────────────┘
└──────────┬───────────────┘                         │
           ▼                                         ▼
┌───────────────────────────────────────────────────────────────────────┐
│                  GRAPH DATABASE + DATA WAREHOUSE                      │
│         Apache AGE / Neo4j (graph)  +  DuckDB (analytical)           │
└──────────────────────────────┬────────────────────────────────────────┘
                               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                     ANALYTICS & ML ENGINE                             │
│  Pattern Detection · Anomaly Scoring · Forecasting · Clustering      │
│  Bias Detection · Model Registry · Explainability (SHAP/LIME)        │
└──────────────┬───────────────────────────────────┬────────────────────┘
               ▼                                   ▼
┌──────────────────────────┐          ┌─────────────────────────────────┐
│    ALERTING ENGINE       │          │     API GATEWAY                 │
│  Threshold-based alerts  │          │     REST + GraphQL              │
│  SMS · Email · Webhook   │          │     Rate-limited, authenticated │
└──────────────┬───────────┘          └──────────────┬──────────────────┘
               ▼                                     ▼
┌───────────────────────────────────────────────────────────────────────┐
│                           DASHBOARD                                   │
│  District-level maps · Time series · Drill-down · Comparison views   │
│  India shapefiles (state → district → block → village)               │
└───────────────────────────────────────────────────────────────────────┘
               ▼
┌───────────────────────────────────────────────────────────────────────┐
│                    AUDIT & PROVENANCE LAYER                           │
│   Full query logs · Data lineage · Access control · DPDPA trail      │
└───────────────────────────────────────────────────────────────────────┘
```

> For the full technical deep-dive — layer-by-layer specifications, technology stack recommendations, connector interface, and deployment models — see **[ARCHITECTURE.md](ARCHITECTURE.md)**.

---

## Project Structure

```
kalki/
├── README.md
├── LICENSE                       # AGPL-3.0
├── ETHICS.md                     # Operational ethics framework
├── LEGAL.md                      # Legal considerations & compliance
├── ARCHITECTURE.md               # Technical architecture deep-dive
├── DATA_SOURCES.md               # Living data source registry
├── CONTRIBUTING.md               # How to contribute
├── GOVERNANCE.md                 # Project governance model
├── CODE_OF_CONDUCT.md            # Community code of conduct
│
├── connectors/                   # Data source connectors
│   ├── README.md                 # Connector development guide
│   ├── base_connector.py         # Abstract base class
│   ├── imd/                      # India Meteorological Department
│   ├── ndma/                     # National Disaster Management Authority
│   ├── data_gov_in/              # data.gov.in OGD Platform
│   ├── cpcb/                     # Central Pollution Control Board
│   └── ...                       # One directory per data source
│
├── modules/
│   ├── kalki_prakriti/            # 🌿 Climate & Disaster (MVP)
│   ├── kalki_shiksha/             # 📚 Education
│   ├── kalki_swastha/             # 🏥 Health & Epidemiology
│   ├── kalki_artha/               # 💰 Economic Stress
│   ├── kalki_nagrik/              # 🏙️ Civic Infrastructure
│   ├── kalki_samaj/               # 👥 Social & Demographic
│   ├── kalki_dharma/              # ⚖️ Governance & Transparency
│   └── kalki_crime/               # 🔍 Crime Patterns (build last)
│
├── ontology/                     # India-specific data taxonomy
├── analytics/                    # Shared analytics engine
├── dashboard/                    # Frontend visualization
├── alerting/                     # Notification engine
├── audit/                        # Provenance and logging
│
├── docs/
│   ├── signals_matrix.md         # Complete signals reference
│   ├── mvp_roadmap.md            # Detailed MVP plan
│   └── faq.md                    # Frequently asked questions
│
└── tests/                        # Test suite
```

---

## Get Started

### For Contributors

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/kalki.git
cd kalki

# Set up the development environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

pip install -r requirements.txt

# Run tests
pytest

# Pick a module, pick a data source, start building!
```

> 📖 See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full guide, including how to build your first data connector.

### For Researchers & Journalists

Kalki outputs will be accessible through:
- **Dashboard** — Interactive maps and charts with district-level drill-down
- **API** — REST and GraphQL endpoints for programmatic access
- **Data Exports** — CSV and PDF report downloads

*(Coming after MVP launch)*

---

## Roadmap

### Phase 1: Foundation (Months 1-4)
- [ ] Core infrastructure: ingestion layer, data lake, ontology framework
- [ ] Connector interface and 3-5 initial connectors (IMD, NDMA, CPCB, data.gov.in)
- [ ] **KalkiPrakriti MVP**: district-level climate risk dashboard
- [ ] Basic dashboard with India map visualization
- [ ] Ethics Board formation
- [ ] Community setup (Discord, GitHub Discussions, contribution guide)

### Phase 2: Core Modules (Months 5-10)
- [ ] KalkiShiksha: education signals dashboard
- [ ] KalkiSwastha: health & epidemiology signals
- [ ] KalkiArtha: economic stress indicators
- [ ] 15+ data connectors built by community
- [ ] API gateway launch
- [ ] Alerting engine (basic threshold alerts)

### Phase 3: Advanced Modules (Months 11-18)
- [ ] KalkiNagrik: civic infrastructure monitoring
- [ ] KalkiSamaj: social & demographic signals
- [ ] KalkiDharma: governance transparency
- [ ] Cross-module correlation engine
- [ ] ML/forecasting pipeline
- [ ] Localization (Hindi, Tamil, Bengali)

### Phase 4: Scale & Governance (Months 18+)
- [ ] KalkiCrime: crime pattern analysis (with full Ethics Board review)
- [ ] Government integration partnerships
- [ ] Institutional partnerships (IITs, research institutes)
- [ ] Consider non-profit foundation formation
- [ ] Mobile-first dashboard redesign

---

## Data Sources

Kalki uses only **publicly accessible** data sources. Every source is documented with accessibility ratings, format details, update frequency, and quality scores.

> 📊 See the complete **[Data Source Registry](DATA_SOURCES.md)** — a living document that rates every source and tracks connector status.

Key sources include:

| Source | Module | Access | Format | Freshness |
|---|---|---|---|---|
| IMD (mausam.imd.gov.in) | Prakriti | ✅ Open | API + HTML | ⚡ Real-time |
| NDMA (ndma.gov.in) | Prakriti | ✅ Open | HTML | Monthly |
| CPCB AQI (cpcb.nic.in) | Prakriti, Swastha | ✅ Open | API | ⚡ Real-time |
| UDISE+ (udiseplus.gov.in) | Shiksha | ✅ Open | HTML + Excel | Annual |
| NREGASoft (nrega.nic.in) | Dharma | ✅ Open | HTML | Daily |
| data.gov.in | All | ✅ Open | CSV + API | Varies |
| RBI Aggregates (rbi.org.in) | Artha | ✅ Open | Excel + PDF | Monthly |
| NCRB (ncrb.gov.in) | Crime | ✅ Open | PDF + Excel | ⏳ 2-3yr delay |

---

## Limitations & Safety

**What Kalki is:**
- A decision-support tool that surfaces patterns from public data
- An aggregation and visualization platform
- A community-driven open-source project

**What Kalki is NOT:**
- A surveillance system
- A predictive policing tool
- A replacement for human judgment
- An authoritative source of truth
- An enforcement mechanism

**Important caveats:**
- Kalki outputs are **indicators**, not **predictions**. They show patterns, not certainties.
- Indian government data has known quality issues: delays, inconsistencies, gaps. Kalki cannot be more accurate than its sources.
- All models carry inherent biases. We audit for these, but perfection is not possible — human review is always required.
- Kalki does not and will never claim predictive certainty.

---

## Governance

Kalki is governed by a community model designed for transparency and scale:

- **Project Founder** — Sets vision and protects mission. Constitutional authority, not executive.
- **Core Team** — Trusted maintainers with cross-module authority. Earned through contribution.
- **Module Maintainers** — Own their module's roadmap and reviews.
- **Ethics Board** — Independent body with veto power on data sources and signal types.
- **Contributors** — Anyone who submits a merged PR. Clear pathway to maintainer and core team.

Government agencies are welcome as **data partners, domain advisors, and users** — but never as controllers of the project's direction.

> 📜 See **[GOVERNANCE.md](GOVERNANCE.md)** for the complete governance model, decision-making processes, and government integration path.

---

## Legal

Kalki operates within Indian law, including:
- **DPDPA 2023** — Digital Personal Data Protection Act compliance
- **RTI Act, 2005** — Data acquisition through Right to Information
- **IT Act, 2000** — Awareness of government powers and responsible disclosure

> ⚖️ See **[LEGAL.md](LEGAL.md)** for the complete legal framework.

---

## License

Kalki is licensed under the **[GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE)**.

**Why AGPL?** Because if anyone takes this code, modifies it, and deploys it as a service, they must share their modifications. This prevents Kalki from being forked into a closed-source surveillance tool.

---

## Contributing

Kalki needs **you**. Whether you're a data engineer, ML researcher, frontend developer, domain expert, journalist, or someone who just knows how to parse Indian government PDFs — there is a place for you here.

### Highest-Impact First Contribution

**Build a data connector.** Pick a government data source from the [Data Source Registry](DATA_SOURCES.md), write a connector using the [standard interface](ARCHITECTURE.md#connector-interface-specification), and submit a PR. You'll have made a real contribution to India's data infrastructure in a weekend.

> 🚀 See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full guide.

---

<p align="center">
  <strong>Kalki is not a product. It is an invitation.</strong>
</p>

<p align="center">
  An invitation to build something India needs — in the open, with integrity,<br/>
  for the people who need early signals most.
</p>

<p align="center">
  <em>If you believe that public data should serve the public,<br/>
  and that India deserves tools built with its own values —<br/>
  join us.</em>
</p>

<p align="center">
  <a href="CONTRIBUTING.md"><strong>Start Contributing →</strong></a>
</p>
