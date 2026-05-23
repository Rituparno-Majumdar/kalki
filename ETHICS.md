# Kalki Ethics Framework

**Kalki: India's Open Intelligence Platform**
**Version**: 1.0
**Effective Date**: May 2026
**Classification**: Operational — Binding on all contributors, modules, and deployments

---

## 1. Preamble

India is the world's largest democracy, home to 1.4 billion people spanning thousands of communities, languages, religions, and cultural traditions. Building an intelligence and forecasting platform in this context is not a neutral technical exercise — it is an act that carries profound ethical weight.

Data aggregation, even from entirely public sources, can reveal patterns about communities and populations that, if misused, can cause real-world harm. History — both in India and globally — demonstrates that analytical tools built without ethical guardrails inevitably become instruments of oppression, discrimination, and surveillance.

**Kalki exists to strengthen democratic accountability, not to undermine it.**

This Ethics Framework is not a collection of aspirational principles. It is an **operationally enforceable document** that governs every aspect of Kalki's design, development, deployment, and use. Violations of this framework are grounds for contributor removal, feature rollback, and public disclosure.

Every contributor, every module, and every deployment of Kalki is bound by this framework. No technical achievement, analytical insight, or community demand justifies deviation from these principles.

---

## 2. Non-Negotiable Principles

### 2.1 Public Data Only

All data processed by Kalki must originate from **publicly accessible sources** that do not require circumventing access controls, authentication barriers, or terms of service.

- Data sources must be legally and ethically accessible to any member of the public
- No scraped private data, leaked databases, hacked systems, or unauthorized access — under any circumstances
- Every data source is documented in `DATA_SOURCES.md` with full provenance: origin, license, access method, and date acquired
- Contributors who introduce data of questionable provenance face immediate review and potential removal

### 2.2 Privacy-First Design

Privacy is a **design constraint**, not an afterthought or optional feature.

- No personal identifiers (names, addresses, phone numbers, Aadhaar numbers, PAN numbers) are stored in processed outputs
- All data pipelines must pass a **Privacy Impact Assessment** before deployment to production
- Privacy is evaluated at every stage: ingestion, processing, storage, output, and visualization
- Default configuration is always the most privacy-protective option

### 2.3 Human-in-the-Loop Decision Making

No Kalki output intended for public consumption is published without human review.

- Automated analysis produces **drafts**, never final outputs
- All published outputs carry clear labeling: `Machine-Generated Draft` or `Human-Reviewed`
- Reviewers must have domain context — a crime analytics output must be reviewed by someone who understands crime data limitations
- The human reviewer bears responsibility for the published output and is identified in the audit trail

### 2.4 No Autonomous Punishment, Enforcement, or Surveillance

Kalki is an **analytical tool**, not an enforcement mechanism.

- Outputs must never be used for autonomous action against individuals or groups
- No Kalki module shall be integrated with enforcement systems, policing tools, or surveillance infrastructure
- Outputs are framed as indicators for further human investigation, never as conclusions warranting action
- Any deployment that uses Kalki outputs for enforcement purposes violates this framework

### 2.5 No Raw Personal Data Exposure

Raw data containing personal information must be processed through anonymization pipelines before any analytical use.

- No output shall contain information sufficient to identify a specific individual
- Quasi-identifiers (unique combinations of age, location, occupation, etc.) must be suppressed or generalized
- If anonymization is not possible for a dataset, the dataset is not used
- Regular re-identification risk assessments are conducted on all outputs

### 2.6 Aggregate-Level Analysis Only

All Kalki outputs operate at the aggregate level — patterns, trends, risk indicators, and statistical summaries.

- No individual profiling, no person-level scoring, no individual risk assessment
- Minimum aggregation thresholds are enforced at the platform level (see Section 3)
- Outputs that could be narrowed to identify individuals are automatically suppressed
- "Zoom and enhance" functionality on individual records is architecturally impossible — by design

### 2.7 Open Collaboration with Clear Documentation

Transparency is non-negotiable for a project that analyzes public data for public interest.

- All methodologies, algorithms, and data transformations are documented in the repository
- The community can inspect, critique, and improve every component
- No black-box models are deployed in production without accompanying explainability documentation
- Model cards are maintained for every analytical model, documenting training data, methodology, limitations, and known biases

---

## 3. DPDPA 2023 Compliance

The Digital Personal Data Protection Act, 2023 governs the processing of digital personal data in India. Even though Kalki processes publicly available data, DPDPA compliance is essential because **aggregated public data can be re-identified** when combined with external datasets.

### 3.1 k-Anonymity Guarantees

Kalki enforces minimum aggregation thresholds to prevent re-identification. No output is generated for groups below these thresholds:

| Data Category | Minimum Group Size | Additional Safeguards |
|---|---|---|
| Crime statistics | 100 individuals | District-level minimum granularity |
| Demographic analysis | 500 individuals | Suppression of outlier groups |
| Governance metrics | N/A (institutional data) | No individual official profiling |
| Social indicators | 200 individuals | Community-level aggregation |
| Economic indicators | 100 entities | Sector-level minimum granularity |
| Environmental/health | 200 individuals | Block-level minimum granularity |

These thresholds are enforced programmatically. Outputs that fail threshold checks are suppressed automatically and flagged for review.

### 3.2 Differential Privacy

For sensitive outputs — particularly those involving crime, health, or demographic data — Kalki applies differential privacy techniques:

- Calibrated noise injection to prevent re-identification from aggregate statistics
- Privacy budget (epsilon) tracked per dataset and per query session
- Sensitivity analysis conducted for all statistical queries
- Privacy loss accumulation monitored across repeated queries on the same data

### 3.3 Purpose Limitation

Data processing purposes are clearly defined per module and documented:

| Module | Stated Purpose | Data Categories |
|---|---|---|
| KalkiCrime | Aggregate crime pattern analysis for public safety research | NCRB data, court records, news reports |
| KalkiDharma | Government spending and governance transparency analysis | Budget data, tender records, project tracking |
| KalkiSamaj | Social development indicator tracking and gap analysis | Census, NFHS, education, health statistics |
| KalkiVayu | Environmental monitoring and public health correlation | Pollution data, weather, health indicators |
| KalkiArtha | Economic indicator analysis and trend forecasting | Economic surveys, trade data, market statistics |

Data acquired for one module **cannot be repurposed** for another without Ethics Board review and documented justification.

### 3.4 Cross-Border Data Processing

- All data processing occurs on **Indian infrastructure**
- No personal or potentially re-identifiable data is transferred outside India
- Contributors outside India work exclusively with anonymized, aggregated datasets
- Cloud infrastructure, if used, must be hosted in Indian data centers

### 3.5 Data Fiduciary Obligations

While Kalki's rigorous anonymization approach aims to avoid triggering Data Fiduciary status under DPDPA, the project operates as if these obligations apply:

- Data minimization: collect only what is necessary for stated purposes
- Accuracy: maintain data quality and document known limitations
- Storage limitation: no indefinite retention of potentially re-identifiable data
- Regular compliance audits conducted by the Ethics Board

---

## 4. Bias Detection & Fairness Auditing

Indian public data carries deep structural biases rooted in the country's complex social history. Caste, gender, religion, urban/rural divides, linguistic identity, economic class, and tribal status all influence how data is collected, what is recorded, and what is invisible.

**Kalki does not treat public data as neutral ground truth.** Every dataset reflects the biases of the systems that generated it.

### 4.1 Mandatory Fairness Audit

Every module output must pass a fairness review before release. This is not optional — it is a required step in the output pipeline.

- Fairness audit results are documented and published alongside the output
- Outputs that fail fairness review are held until bias is addressed or adequately disclosed
- Fairness audit methodology is documented and open to community critique

### 4.2 Demographic Baseline Testing

Every heatmap, risk zone, signal, or spatial output must be tested against demographic baselines:

- Crime heatmaps cross-referenced with Census demographic data
- Economic indicators tested for urban/rural bias
- Health data tested for gender and caste disparities in reporting
- Governance metrics tested for regional and linguistic representation

### 4.3 Correlation Flagging

> **Operational Rule**: If any spatial or categorical output correlates with a protected characteristic at r > 0.3 (Pearson correlation coefficient), the output is **automatically held** for Ethics Board review before publication. The correlation, its magnitude, and potential explanations must be documented.

This rule exists because statistical correlation between risk indicators and demographic characteristics often reflects systemic inequality — not actual risk. Publishing such correlations without context can reinforce discrimination.

### 4.4 Protected Characteristics

| Protected Characteristic | Monitoring Approach | Correlation Threshold |
|---|---|---|
| Caste | Cross-reference with Census caste demographics | r > 0.3 |
| Religion | Cross-reference with Census religious demographics | r > 0.3 |
| Gender | Disaggregated analysis mandatory for all outputs | r > 0.3 |
| Tribal Status (ST/PVTG) | Enhanced protection — particularly vulnerable populations | r > 0.2 |
| Linguistic Identity | Regional language distribution analysis | r > 0.3 |
| Economic Class | Income and poverty indicator cross-reference | r > 0.3 |
| Urban/Rural | Settlement type distribution analysis | r > 0.3 |

### 4.5 Fairness Metrics

The following quantitative fairness metrics are computed for every output:

- **Statistical Parity Difference**: measures whether outcomes are equally distributed across groups
- **Equalized Odds**: measures whether error rates are consistent across groups
- **Disparate Impact Ratio**: ratio of positive outcome rates between groups (threshold: 0.8-1.25)
- **Calibration**: measures whether predicted probabilities match observed frequencies across groups

### 4.6 Remediation

When bias is detected:

1. Output is immediately held from publication
2. Root cause analysis: is the bias in the data, the methodology, or the framing?
3. Methodology revised if bias stems from analytical approach
4. If bias is inherent in source data, output published with prominent contextual disclosure
5. All findings documented in the module's bias audit log
6. Community notified of the finding and the remediation

---

## 5. Ethics Board Charter

### 5.1 Composition

The Ethics Board consists of **7 seats** with rotating 2-year terms, staggered to ensure continuity:

| Seat | Expertise Required | Selection Method |
|---|---|---|
| 1 | Civil liberties lawyer (constitutional law focus) | Nominated by legal community organizations |
| 2 | Data privacy expert (DPDPA-familiar) | Community nomination and vote |
| 3 | Social scientist (India focus — caste, gender, inequality) | Academic institution nomination |
| 4 | Investigative data journalist | Media community nomination |
| 5 | Government/policy domain expert | Community nomination and vote |
| 6 | Civil society organization representative | CSO network nomination |
| 7 | Technical ethics researcher (AI/ML fairness) | Academic/community nomination |

**Diversity requirement**: The Board must include representation from at least 3 different Indian states/regions and at least 3 different gender identities.

### 5.2 Responsibilities

- **Review and approve** new data source integrations before they enter production
- **Review new signal types** and analytical methodologies for ethical implications
- **Audit model outputs** for bias — quarterly at minimum, or on-demand when flagged
- **Veto power** on features, outputs, or modules that violate ethical principles
- **Publish quarterly transparency reports** detailing reviews conducted, issues found, and actions taken
- **Respond to Right to Contest requests** within 30 days
- **Review and update** this Ethics Framework annually

### 5.3 Governance

- **Cadence**: quarterly review sessions; additional sessions as needed
- **Emergency review**: any Board member can trigger an emergency review, convened within 48 hours
- **Terms**: 2-year rotating terms; maximum 2 consecutive terms; staggered so no more than 4 seats turn over simultaneously
- **Independence**: the Board is advisory to the community, not controlled by any contributor, organization, funder, or government entity
- **Decisions**: simple majority (4 of 7) for standard decisions; supermajority (5 of 7) for vetoes and framework amendments
- **Transparency**: all deliberations documented and published, with appropriate redactions for sensitive cases involving individuals
- **Conflicts of interest**: Board members must recuse themselves from decisions where they have a personal or organizational interest

---

## 6. Audit Trail Requirements

Every interaction with Kalki's analytical capabilities is logged to maintain accountability and enable oversight.

### 6.1 Query Logging

Every query is logged with the following fields:

| Field | Description | Example |
|---|---|---|
| `timestamp` | ISO 8601 timestamp with timezone | `2026-05-23T12:00:00+05:30` |
| `user_id` | Anonymized user identifier | `usr_a7b3c9` |
| `query_type` | Type of query performed | `crime_heatmap` |
| `module` | Kalki module accessed | `KalkiCrime` |
| `parameters` | Query parameters (sanitized) | `{"district": "Mumbai", "year": 2025}` |
| `results_summary` | Summary of results returned | `47 district-level records` |
| `data_sources` | Sources used for this query | `[NCRB, Census 2021]` |
| `review_status` | Human review status | `pending` / `reviewed` / `flagged` |
| `fairness_check` | Bias audit result | `passed` / `held_for_review` |

### 6.2 Data Lineage

Every insight, visualization, or output is traceable to its source data through a documented pipeline:

- Source dataset → ingestion pipeline → transformation steps → aggregation → output
- Each step is versioned and reproducible
- Lineage metadata is stored alongside the output

### 6.3 Retention and Access

- **Retention**: audit logs retained for a minimum of **3 years**
- **Access**: audit logs accessible to the Ethics Board, Core Team, and during authorized external audits
- **Immutability**: audit logs are append-only — no modification or deletion permitted
- **Format**: structured JSON logging with a standardized schema
- **Storage**: audit logs stored separately from analytical data, with independent access controls

---

## 7. Right to Contest

Any community, administrator, organization, or affected group that is flagged, highlighted, or characterized by Kalki outputs has the right to contest those outputs.

### 7.1 Who Can Contest

- Communities or populations described in Kalki outputs
- Local administrators or government officials referenced in governance analytics
- Organizations mentioned or implicated in any output
- Civil society organizations acting on behalf of affected communities
- Any individual who believes Kalki outputs could cause harm to their community

### 7.2 Contest Process

1. **Submit Request**: via designated channel — GitHub issue using the Contest Template, or email to ethics@kalki-project.org
2. **Acknowledgment**: Ethics Board acknowledges receipt within **7 days**
3. **Interim Measures**: contested output is **immediately paused** — removed from public display pending review
4. **Investigation**: Ethics Board conducts full review within **30 days**, including methodology audit and data verification
5. **Decision**: public response published with findings, rationale, and any corrective action
6. **Remediation**: if contest is upheld — output corrected or withdrawn, methodology revised, and a public correction issued

### 7.3 Protections

- **No Retaliation**: contesting an output shall never result in negative consequences for the contester
- **Confidentiality**: contester identity protected if requested
- **Good Faith**: contests made in good faith are always welcome, even if ultimately not upheld
- **Transparency**: all contest decisions (anonymized if necessary) are published in quarterly transparency reports

---

## 8. Data Retention & Deletion Policy

### 8.1 Retention Schedule

| Data Type | Retention Period | Deletion Process |
|---|---|---|
| Raw public data | Duration of source availability | Automated expiry with source monitoring |
| Processed aggregates | 5 years | Version-controlled deletion with audit trail |
| Personally attributable data | 2 years maximum | Mandatory deletion — no exceptions |
| Audit logs | 3 years minimum | Archived securely after retention period |
| Model artifacts | Life of model version | Deleted upon model retirement |
| Contest records | 5 years | Archived with anonymization |

### 8.2 Principles

- **Raw Data**: retained only as long as the original source permits and remains publicly available
- **Processed Data**: versioned with semantic versioning; deletion procedures documented and auditable
- **No Indefinite Retention**: personally attributable data — even if derived from public sources — has a maximum retention of **2 years**
- **Deletion Requests**: honored within **30 days** for any data that could identify individuals
- **Archival**: historical aggregated data may be retained for trend analysis, subject to re-anonymization review before each retention renewal

---

## 9. Module-Specific Ethics

### 9.1 KalkiCrime — Crime Analytics

Crime data is among the most sensitive categories Kalki processes. Misuse of crime analytics can stigmatize communities, reinforce discriminatory policing, and cause lasting harm.

- **District-level minimum aggregation** — no sub-district crime mapping permitted
- **Mandatory demographic bias check** on every output before publication
- **Read-only analytics** — no real-time tracking, no live feeds, no streaming data
- **Ethics Board reviews every new signal type** before it is deployed
- **Contextual framing**: crime data always presented alongside socioeconomic indicators (poverty rates, unemployment, urbanization) to prevent decontextualized interpretation
- **No predictive outputs**: KalkiCrime analyzes historical patterns — it does not predict future crimes or identify potential offenders

### 9.2 KalkiDharma — Governance Analytics

Governance analytics must balance transparency with fairness. Flagging anomalies is necessary; making accusations is not Kalki's role.

- Report anomalies as **flags for investigation**, never as **accusations of wrongdoing**
- **Human review required** before any governance output is published
- Focus on **institutional patterns** (department-level, scheme-level) — not individual officials
- All governance outputs carry an explicit disclaimer: *"This is an analytical indicator based on public data. It is not an accusation, finding of fact, or legal determination."*
- Contextual factors (regional capacity, historical patterns, data quality) documented alongside every flag

### 9.3 KalkiSamaj — Social Analytics

Social analytics about India's diverse communities must be handled with exceptional care. Outputs must empower, not stigmatize.

- **Frame all outputs as support and prevention** — never punishment or blame
- **Enhanced privacy protections** for vulnerable populations (Scheduled Tribes, PVTGs, religious minorities, LGBTQ+ communities)
- **Community consultation** before publishing sensitive social indicators about identifiable communities
- **No caste-based, religion-based, or tribe-based profiling** — analysis is at the indicator level, not the community level
- Social data always presented with historical context and systemic factors

### 9.4 All Other Modules

- The full Ethics Framework applies to all modules without exception
- New modules must submit an **Ethics Impact Assessment** before development begins
- The Ethics Impact Assessment template is maintained in `docs/templates/ethics-impact-assessment.md`
- Modules that process data about people (even indirectly) undergo enhanced review

---

## 10. Red Lines — Things Kalki Will Never Do

> **These are absolute prohibitions. No exception. No override. No emergency justification. No "just this once."**

- **Individual tracking or profiling** — Kalki does not track, monitor, or profile individuals. Period.
- **Real-time surveillance** — Kalki does not operate in real-time on personal data or behavioral streams.
- **Predictive policing at individual level** — Kalki does not predict who will commit crimes or identify "potential offenders."
- **Sharing data with law enforcement for targeting** — Kalki does not serve as a law enforcement intelligence tool. Outputs are for public understanding, not prosecution.
- **Facial recognition or biometric analysis** — Kalki does not process, store, or analyze biometric data of any kind.
- **Social credit scoring** — Kalki does not score, rank, or rate individuals or communities on behavioral or social metrics.
- **Automated decision-making without human review** — Every output that reaches the public has been reviewed by a qualified human. No exceptions.
- **Processing private communications** — Kalki does not access, intercept, store, or analyze private messages, emails, phone calls, or any form of private communication.
- **Caste-based or religion-based targeting** — Kalki will never produce outputs designed to target, stigmatize, or discriminate against any caste, religious, tribal, or linguistic community.
- **Enabling authoritarian control** — Kalki will never be modified, deployed, or licensed for use by any entity seeking to suppress democratic freedoms, target dissidents, or control populations.

> **Violation of any Red Line is grounds for immediate feature removal, contributor permanent ban, and public disclosure of the violation.**

---

*This document is maintained by the Kalki Core Team and Ethics Board. Changes require Ethics Board approval and a community review period of 30 days. No amendment may weaken the Red Lines defined in Section 10.*

*Last updated: May 2026 | Version: 1.0 | License: CC-BY-SA-4.0*
