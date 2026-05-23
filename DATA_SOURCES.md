# Kalki — Data Source Registry

> **Version:** 0.1.0-draft
> **Last Updated:** 2026-05-23
> **Status:** Living Document — contributions welcome
> **Maintainers:** Community-maintained via Pull Requests

---

## Table of Contents

- [About This Document](#about-this-document)
- [Rating Legend](#rating-legend)
- [Sources by Module](#sources-by-module)
  - [KalkiPrakriti — Climate and Disaster (MVP)](#kalkiprakriti--climate-and-disaster)
  - [KalkiArtha — Economic Stress](#kalkiartha--economic-stress)
  - [KalkiSwastha — Health and Epidemiology](#kalkiswastha--health-and-epidemiology)
  - [KalkiShiksha — Education](#kalkishiksha--education)
  - [KalkiSamaj — Social and Demographic](#kalkisamaj--social-and-demographic)
  - [KalkiDharma — Governance and Transparency](#kalkidharma--governance-and-transparency)
  - [KalkiNagrik — Civic Infrastructure](#kalkinagrik--civic-infrastructure)
  - [KalkiCrime — Crime Patterns (Build Last)](#kalkicrime--crime-patterns)
- [Cross-Module Sources](#cross-module-sources)
- [Aspirational Sources](#aspirational-sources)
- [How to Add a New Data Source](#how-to-add-a-new-data-source)
- [Data Source Health Monitoring](#data-source-health-monitoring)

---

## About This Document

This is the **canonical registry of all data sources** that Kalki ingests or plans to ingest. It serves three purposes:

1. **For developers:** Understand what data is available, in what format, and how hard it is to work with before building a connector.
2. **For contributors:** Find a data source that needs a connector and start building.
3. **For users:** Understand the provenance and quality of data powering Kalki's intelligence.

**This is a living document.** Contributors are encouraged to:
- Add new data sources they discover
- Update ratings as sources change (APIs added, formats updated, sources go offline)
- Correct inaccuracies
- Add notes about quirks, gotchas, and workarounds

All changes should be submitted via Pull Request with evidence of accessibility (screenshot, API response, or documentation link).

---

## Rating Legend

### Accessibility

| Icon | Rating | Description |
|---|---|---|
| ✅ | Open | Free to access, no authentication required |
| 🔑 | Registration | Requires free registration or API key |
| ⚠️ | RTI Required | Data exists but may need Right to Information request |
| ❌ | Restricted | Paid, restricted to government users, or not publicly available |

### Format

| Icon | Format | Difficulty |
|---|---|---|
| 🔌 | API | Easiest — structured, programmatic access |
| 📊 | CSV / Excel | Moderate — structured but schema varies |
| 📄 | PDF | Hard — requires parsing, often tables in PDF |
| 🌐 | HTML Scrape | Hard — fragile, breaks when site redesigns |
| 🖼️ | Scanned Image | Hardest — requires OCR, error-prone |

### Freshness

| Icon | Frequency | Description |
|---|---|---|
| ⚡ | Real-time | Updates within minutes |
| 📅 | Daily | Updates once per day |
| 📆 | Weekly / Monthly | Updates weekly or monthly |
| 📋 | Quarterly | Updates every 3 months |
| 📌 | Annual | Updates once per year |
| ⏳ | Delayed | Data is 2+ years behind current date |

### Granularity

| Icon | Level | Description |
|---|---|---|
| 🇮🇳 | National | Country-level aggregates only |
| 🏛️ | State | State / Union Territory level |
| 📍 | District | District level (primary working level for Kalki) |
| 🏘️ | Block / Panchayat | Sub-district level |
| 🏠 | Village / Ward | Lowest administrative unit |

### Quality

| Icon | Rating | Description |
|---|---|---|
| 🟢 | High | Consistent schema, reliable updates, good coverage |
| 🟡 | Medium | Usable but has gaps, inconsistencies, or format issues |
| 🔴 | Low | Significant issues — missing data, broken formats, unreliable |

### Connector Status

| Icon | Status | Description |
|---|---|---|
| ✅ | Built | Connector implemented, tested, and in production |
| 🔨 | In Progress | Connector actively being developed |
| 📋 | Planned | On the roadmap but not yet started |
| 🆘 | Needs Contributor | No one is working on this — help wanted! |

---

## Sources by Module

### KalkiPrakriti 🌿 — Climate and Disaster

> **Status:** MVP Module — build this first
>
> **Purpose:** Climate monitoring, disaster risk assessment, environmental intelligence at district level across India.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| IMD Weather Data | mausam.imd.gov.in | India Meteorological Department | ✅ Open | 🔌 API + 🌐 HTML | ⚡ Real-time | 📍 District | 🟢 High | 🆘 Needs Contributor |
| NDMA Disaster Data | ndma.gov.in | National Disaster Management Authority | ✅ Open | 🌐 HTML | 📆 Monthly | 🏛️ State | 🟡 Medium | 🆘 Needs Contributor |
| CPCB AQI | cpcb.nic.in | Central Pollution Control Board | ✅ Open | 🔌 API | ⚡ Real-time | 📍 Station-level | 🟢 High | 🆘 Needs Contributor |
| Bhuvan (ISRO) | bhuvan.nrsc.gov.in | Indian Space Research Organisation | ✅ Open | 🔌 API + 📊 GeoTIFF | 📅 Daily | 📍 Pixel-level | 🟢 High | 🆘 Needs Contributor |
| IUDX | iudx.org.in | Smart Cities Mission | 🔑 Registration | 🔌 API | ⚡ Real-time | 📍 City-level | 🟡 Medium | 🆘 Needs Contributor |
| data.gov.in (Climate) | data.gov.in | NIC / MeitY | ✅ Open | 📊 CSV + 🔌 API | 📆 Monthly | 🏛️ State / 📍 District | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- IMD has both a web-based data portal and undocumented API endpoints. The API returns JSON but is not officially documented. Connector should handle both.
- CPCB AQI API is well-structured but occasionally returns stale readings without updating timestamps. Connector must cross-validate freshness.
- Bhuvan provides WMS/WFS endpoints for satellite data. GeoTIFF downloads require understanding ISRO's tile naming convention.
- NDMA data is mostly narrative reports on the website. Structured historical data requires scraping from annual reports (PDFs).

---

### KalkiArtha 💰 — Economic Stress

> **Purpose:** Economic early warning — track employment, prices, credit stress, fiscal flows, and agricultural economics at granular levels.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| RBI Aggregates | rbi.org.in | Reserve Bank of India | ✅ Open | 📊 Excel + 📄 PDF | 📆 Monthly | 🏛️ State | 🟢 High | 🆘 Needs Contributor |
| AgMarkNet | agmarknet.gov.in | Directorate of Marketing & Inspection | ✅ Open | 🌐 HTML + 📊 CSV | 📅 Daily | 📍 Mandi-level | 🟡 Medium | 🆘 Needs Contributor |
| PMFBY (Crop Insurance) | pmfby.gov.in | Ministry of Agriculture | ✅ Open | 🌐 HTML | 📋 Quarterly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| data.gov.in (Economy) | data.gov.in | NIC / MeitY | ✅ Open | 📊 CSV + 🔌 API | Varies | Varies | 🟡 Medium | 🆘 Needs Contributor |
| EPFO (aggregates) | epfindia.gov.in | Ministry of Labour | ✅ Open | 📄 PDF | 📆 Monthly | 🇮🇳 National | 🟡 Medium | 🆘 Needs Contributor |
| MoLE Employment Data | labour.gov.in | Ministry of Labour & Employment | ✅ Open | 📄 PDF + 📊 Excel | 📋 Quarterly | 🏛️ State | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- RBI publishes an enormous amount of data, but almost entirely as Excel workbooks and PDF bulletins. Schemas change between publications. Expect significant parsing work.
- AgMarkNet is one of India's most valuable real-time datasets — daily commodity prices from 7,000+ mandis. However, the website is fragile and the HTML structure changes periodically.
- EPFO publishes only national aggregates publicly. State-level formal employment data may require RTI requests or CMIE (paid).

---

### KalkiSwastha 🏥 — Health and Epidemiology

> **Purpose:** Disease surveillance, health infrastructure assessment, epidemic early warning, and health outcome tracking.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| IDSP (Disease Surveillance) | idsp.nic.in | National Centre for Disease Control | ✅ Open | 📄 PDF + 🌐 HTML | 📆 Weekly | 🏛️ State / 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| HMIS (Health MIS) | hmis.nhp.gov.in | Ministry of Health & Family Welfare | 🔑 Registration | 🌐 HTML | 📆 Monthly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| CPCB AQI (health correlation) | cpcb.nic.in | Central Pollution Control Board | ✅ Open | 🔌 API | ⚡ Real-time | 📍 Station | 🟢 High | 🆘 Needs Contributor |
| State Health Dashboards | Varies by state | State Governments | ✅ Open | 🌐 HTML | Varies | 📍 District | 🔴 Low–🟡 Medium | 🆘 Needs Contributor |
| CoWIN / eSanjeevani | cowin.gov.in | Ministry of Health & Family Welfare | ✅ Open | 🔌 API | 📅 Daily | 📍 District | 🟢 High | 🆘 Needs Contributor |

**Notes:**
- IDSP publishes weekly disease outbreak reports as PDFs. These contain tables of outbreak data by state and district but require PDF parsing. The format has remained relatively stable.
- HMIS is a rich dataset covering maternal health, immunization, hospital infrastructure, etc. Requires free registration. Data is served via a web dashboard with no API — scraping required.
- State health dashboards vary enormously in quality, format, and availability. Some states (Kerala, Tamil Nadu) have excellent dashboards; others have minimal or broken ones. Each state will need its own sub-connector.
- CoWIN has a well-documented API that was built during COVID-19. Check if endpoints remain active for ongoing vaccination data.

---

### KalkiShiksha 📚 — Education

> **Purpose:** Track educational infrastructure, learning outcomes, enrollment patterns, and teacher availability.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| UDISE+ | udiseplus.gov.in | Ministry of Education | ✅ Open | 🌐 HTML + 📊 Excel | 📌 Annual | 📍 School-level | 🟢 High | 🆘 Needs Contributor |
| NAS (National Achievement Survey) | nas.gov.in | NCERT | ✅ Open | 📄 PDF + 📊 Excel | 📌 Periodic | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| data.gov.in (Education) | data.gov.in | NIC / MeitY | ✅ Open | 📊 CSV | Varies | Varies | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- UDISE+ is India's most comprehensive education dataset, covering every school in the country. Data is published annually via a web portal with downloadable reports. School-level granularity is exceptional but the dataset is massive.
- NAS provides learning outcome assessments at district level, published periodically (not annual). Results are published as PDF reports with data tables.
- data.gov.in has various education-related datasets but they are often outdated or duplicates of UDISE+ data.

---

### KalkiSamaj 👥 — Social and Demographic

> **Purpose:** Demographic baselines, nutrition, gender indicators, and social development metrics.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| Census of India | censusindia.gov.in | Registrar General of India | ✅ Open | 📊 Excel + 📄 PDF | 📌 Decadal | 🏠 Village | 🟢 High (but 2011 data) | 🆘 Needs Contributor |
| NFHS (National Family Health Survey) | rchiips.org/nfhs | Ministry of Health & Family Welfare | ✅ Open | 📄 PDF + 📊 Data | 📌 Periodic | 🏛️ State / 📍 District | 🟢 High | 🆘 Needs Contributor |
| POSHAN Abhiyaan | poshanabhiyaan.gov.in | Ministry of Women & Child Development | ✅ Open | 🌐 HTML | 📆 Monthly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| NCW (Complaints Data) | ncw.nic.in | National Commission for Women | ✅ Open | 🌐 HTML + 📄 PDF | 📆 Monthly | 🏛️ State | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- Census 2011 remains the most granular demographic dataset for India. Census 2021 has been delayed. The 2011 data is downloadable as Excel files with village-level granularity.
- NFHS-5 (2019–2021) provides district-level data on health, nutrition, gender, and demographics. Fact sheets are PDFs; microdata is available for registered researchers.
- POSHAN Abhiyaan dashboard tracks nutrition indicators at district level. Data is served via a web dashboard that requires scraping.

---

### KalkiDharma ⚖️ — Governance and Transparency

> **Purpose:** Track government fund flows, scheme implementation, public procurement, and fiscal transparency.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| NREGASoft | nrega.nic.in | Ministry of Rural Development | ✅ Open | 🌐 HTML | 📅 Daily | 🏘️ Panchayat | 🟢 High | 🆘 Needs Contributor |
| GeM (Govt e-Marketplace) | gem.gov.in | Ministry of Commerce & Industry | ✅ Open | 🌐 HTML + 📊 Dashboard | 📅 Daily | 🇮🇳 National | 🟡 Medium | 🆘 Needs Contributor |
| PFMS (Public Financial Mgmt) | pfms.nic.in | Controller General of Accounts | ✅ Open | 🌐 HTML | 📆 Monthly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| DBT Bharat | dbtbharat.gov.in | Cabinet Secretariat | ✅ Open | 🌐 HTML | 📆 Monthly | 🏛️ State | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- NREGASoft is one of India's most impressive public data systems. It provides panchayat-level data on MGNREGA employment, wages, and expenditure — updated daily. The website is massive with deeply nested HTML tables. A robust scraper is essential.
- GeM provides procurement data but primarily through dashboards, not downloadable datasets. Scraping required.
- PFMS tracks fund transfers from central government to states and districts. Data is on a web portal that can be scraped.
- DBT Bharat tracks Direct Benefit Transfer across schemes. Dashboard data only — scraping required.

---

### KalkiNagrik 🏙️ — Civic Infrastructure

> **Purpose:** Track drinking water, sanitation, housing, and smart city infrastructure delivery.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| Jal Jeevan Mission | jaljeevanmission.gov.in | Ministry of Jal Shakti | ✅ Open | 🌐 HTML + Dashboard | 📅 Daily | 🏠 Village | 🟢 High | 🆘 Needs Contributor |
| Swachh Bharat Mission | swachhbharatmission.gov.in | Ministry of Housing & Urban Affairs | ✅ Open | 🌐 HTML | 📆 Monthly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |
| Smart City Dashboards | smartcities.gov.in | MoHUA | ✅ Open | 🌐 HTML | Varies | 📍 City | 🟡 Medium | 🆘 Needs Contributor |
| PMAY (Housing) | pmaymis.gov.in | Ministry of Housing & Urban Affairs | ✅ Open | 🌐 HTML | 📆 Monthly | 📍 District | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- Jal Jeevan Mission has one of the best government dashboards in India. Village-level data on tap water connections is updated daily. The dashboard is well-structured but has no API — scraping required.
- Swachh Bharat Mission data covers toilet construction and sanitation progress. District-level data is available via the web portal.
- Smart City dashboards vary by city. The central portal aggregates some metrics but individual city dashboards have richer data.
- PMAY tracks housing construction progress under Pradhan Mantri Awas Yojana. District-level data via web portal.

---

### KalkiCrime 🔍 — Crime Patterns

> **Status:** Build Last — requires careful ethical handling
>
> **Purpose:** Crime trend analysis using only publicly available, aggregate data. No real-time surveillance. No individual case data.
>
> **Important:** CCTNS (Crime and Criminal Tracking Network and Systems) and state police databases are **NOT** listed here. They are restricted law enforcement systems and violate Kalki's public-data-only principle.

| Source | URL | Authority | Access | Format | Freshness | Granularity | Quality | Connector |
|---|---|---|---|---|---|---|---|---|
| NCRB (Crime in India) | ncrb.gov.in | National Crime Records Bureau | ✅ Open | 📄 PDF + 📊 Excel | ⏳ 2–3 year delay | 📍 District | 🟢 High (delayed) | 🆘 Needs Contributor |
| CERT-In Advisories | cert-in.org.in | MeitY | ✅ Open | 🌐 HTML | ⚡ Real-time | 🇮🇳 National | 🟢 High | 🆘 Needs Contributor |
| data.gov.in (Crime) | data.gov.in | NIC / MeitY | ✅ Open | 📊 CSV | Varies | Varies | 🟡 Medium | 🆘 Needs Contributor |

**Notes:**
- NCRB's "Crime in India" annual publication is the gold standard for Indian crime data, but it runs 2–3 years behind. Published as PDF with detailed tables. Excel data tables are also available for recent years.
- CERT-In publishes cybersecurity advisories and vulnerability notes. Useful for cyber threat tracking at national level.
- data.gov.in hosts some crime-related datasets but they are often subsets of NCRB data.
- **Ethical guardrails:** All crime data in Kalki must be aggregate (district-level or above). No individual case data. No predictive policing. See `ETHICS.md`.

---

## Cross-Module Sources

These sources are useful across multiple Kalki modules:

| Source | URL | Authority | Modules | Access | Format | Notes |
|---|---|---|---|---|---|---|
| data.gov.in | data.gov.in | NIC / MeitY | All | ✅ Open | 📊 CSV + 🔌 API | India's central open data portal. Has an API but data freshness varies enormously. Some datasets are years old. |
| Local Government Directory (LGD) | lgdirectory.gov.in | MoPR | All (ontology) | ✅ Open | 🔌 API + 🌐 HTML | **Critical for ontology layer.** Maps administrative codes to names. Provides the canonical ID system for states, districts, blocks, panchayats. |
| Survey of India | surveyofindia.gov.in | DST | All (maps) | ✅ Open | 📊 GeoJSON + Shapefiles | Administrative boundary shapefiles. Essential for map visualizations. Also see Datameet community GeoJSON (open, community-maintained). |
| India Census 2011 | censusindia.gov.in | RGI | All (baseline) | ✅ Open | 📊 Excel + 📄 PDF | Provides the demographic baseline for per-capita calculations, population weighting, and rural/urban classification. |
| Election Commission | eci.gov.in | ECI | Dharma, Samaj | ✅ Open | 🌐 HTML + 📄 PDF | Constituency-level election data. Useful for governance overlay. |
| NITI Aayog | niti.gov.in | NITI Aayog | All | ✅ Open | 📄 PDF + 📊 Dashboard | Publishes composite development indices at district level. SDG India Index. |
| Datameet | datameet.org | Community | All (maps, ontology) | ✅ Open | 📊 GeoJSON + CSV | Community-maintained Indian geographic data, boundary files, and datasets. Invaluable resource. |

---

## Aspirational Sources

These data sources are **not currently accessible** in a form suitable for Kalki, but would be extremely valuable if they become available. The community should track these and pursue access where appropriate.

| Source | Authority | Why Valuable | Current Barrier | Path to Access |
|---|---|---|---|---|
| CCTNS (aggregate APIs) | NCRB / MHA | Real-time crime aggregates at district level | Restricted to law enforcement | Advocate for aggregate public APIs through policy channels |
| CMIE (Consumer Pyramids) | CMIE (private) | Household-level economic panel data | Paid subscription, expensive | Explore academic/NGO tier or open-data advocacy |
| TrackChild | Ministry of WCD | Missing and trafficked children data | Portal exists but data access unclear | Verify if aggregate data is publicly available |
| State Police Portals | State Home Departments | State-level crime data more current than NCRB | No standardized format, many states don't publish | Monitor individual state portals for open data |
| NSSO Microdata | MoSPI | Detailed household survey data | Available with registration and conditions | Apply for researcher access where needed |
| Land Records (BhuLekh) | State Revenue Departments | Land ownership patterns (aggregate only) | State-specific portals, no standard API | Build state-specific scrapers as capacity allows |
| Unified Portal for ONORC | DFPDO | PDS and food security data | Dashboard only, no API | Scrape or advocate for API |

> **Note:** Kalki will only integrate aspirational sources if they can be accessed through **legal, ethical, and publicly sanctioned** channels. No circumvention of access controls.

---

## How to Add a New Data Source

Contributing a new data source to this registry is one of the easiest ways to help Kalki. Here is the process:

### Step 1: Verify the Source

Before adding a source, verify:

- [ ] **Publicly accessible:** Can you access the data without special government credentials?
- [ ] **Legal to use:** Are there Terms of Service that restrict automated access or redistribution?
- [ ] **Relevant:** Does the data serve one or more Kalki modules?
- [ ] **Not a duplicate:** Is this data already covered by an existing source in this registry?
- [ ] **Aggregate data only:** Does the source provide aggregate/statistical data, not individual PII?

### Step 2: Document the Source

Add a row to the appropriate module table with:

| Field | Description |
|---|---|
| Source | Human-readable name of the data source |
| URL | Primary URL where data can be accessed |
| Authority | Government body or organization responsible |
| Access | Accessibility rating (see legend) |
| Format | Primary data format(s) (see legend) |
| Freshness | How frequently the data is updated (see legend) |
| Granularity | Geographic granularity (see legend) |
| Quality | Overall quality rating (see legend) |
| Connector | Current connector status (see legend) |

### Step 3: Add Notes

Below the module table, add notes about:

- Any quirks, gotchas, or known issues with the source
- Whether the format has changed historically
- Rate limiting or access restrictions
- Recommended parsing approach (API, scraper, PDF parser, etc.)
- Any Terms of Service considerations

### Step 4: Submit a Pull Request

- Fork the repository
- Edit `DATA_SOURCES.md`
- Include evidence of accessibility (screenshot, sample data, or documentation link)
- Submit a PR with the title: `data-source: Add <source_name> to <module_name>`
- Tag the PR with the `data-sources` label

---

## Data Source Health Monitoring

As Kalki matures, we will implement automated health monitoring for all data sources with built connectors:

| Metric | Description | Alert Threshold |
|---|---|---|
| **Availability** | Is the source reachable? | 3 consecutive failures |
| **Freshness** | When was data last updated? | 2x expected update frequency |
| **Schema Stability** | Has the data format changed? | Any schema mismatch |
| **Quality Score Trend** | Is data quality degrading? | Score drops below 0.5 |
| **Volume Anomaly** | Is the data volume unusually high or low? | More than 2 standard deviations from mean |

Health status for all sources will be displayed on a dedicated monitoring dashboard and published as a community report monthly.

---

> **Related Documents:**
> - `ARCHITECTURE.md` — How connectors fit into the system architecture
> - `ETHICS.md` — Ethical constraints on data collection and use
> - `CONTRIBUTING.md` — How to build a connector for a data source
> - `README.md` — Project overview and getting started

---

*This is a living document. If you know of a public Indian data source not listed here, please submit a PR. Every source added makes Kalki more capable.*
