# Kalki Legal Considerations

**Kalki: India's Open Intelligence Platform**
**Version**: 1.0
**Effective Date**: May 2026

---

> **IMPORTANT**: This document is **NOT legal advice**. It is a guide for contributors and users to understand the legal landscape relevant to the Kalki project. For specific legal situations, consult a qualified Indian lawyer. Laws referenced here are subject to change — this document will be updated as regulations evolve.

---

## 1. Disclaimer

This document is prepared for informational purposes only. It summarizes relevant Indian laws and regulations that contributors and users of Kalki should be aware of, but it does not constitute legal counsel, create an attorney-client relationship, or guarantee legal protection.

- **Purpose**: inform contributors about the legal landscape affecting open-source public data analytics in India
- **Not a substitute**: for professional legal advice — always consult a qualified advocate for specific situations
- **Laws evolve**: Indian data protection and information technology law is rapidly developing; this document is reviewed quarterly
- **Jurisdictional variation**: contributors operating outside India may face additional or different legal requirements in their home jurisdictions
- **No guarantee**: following this guide does not guarantee legal compliance in all circumstances

---

## 2. DPDPA 2023 — Digital Personal Data Protection Act

The Digital Personal Data Protection Act, 2023 is India's comprehensive data protection law. It governs the processing of digital personal data and introduces obligations for entities that determine the purpose and means of data processing.

### 2.1 Applicability to Public Data

- DPDPA defines "personal data" as any data about an individual who is identifiable by or in relation to such data
- **Publicly available data can still qualify as personal data** under DPDPA — public availability does not automatically exempt data from protection
- Processing public data without safeguards may still trigger DPDPA obligations
- **Kalki's position**: we process aggregated, anonymized public data — not personal data. Our anonymization and aggregation pipelines are designed to ensure that outputs do not constitute personal data under DPDPA

### 2.2 Data Fiduciary Obligations

Under DPDPA, a "Data Fiduciary" is any person who determines the purpose and means of processing personal data. If Kalki processes any data that could be considered personal, it may be treated as a Data Fiduciary.

**Obligations of a Data Fiduciary include**:

- **Purpose limitation**: process data only for stated, lawful purposes
- **Data minimization**: collect only what is necessary
- **Accuracy**: ensure data is correct and up to date
- **Storage limitation**: retain data only as long as necessary
- **Reasonable security safeguards**: protect data from breaches

**Kalki's approach**: avoid triggering Data Fiduciary status entirely through rigorous anonymization at the point of ingestion, ensuring no personal data persists in our systems.

### 2.3 Purpose Limitation

DPDPA requires that data be processed only for the specific purposes for which it was collected or for which consent was obtained. Each Kalki module has a clearly defined and documented purpose:

| Module | Stated Purpose |
|---|---|
| KalkiCrime | Aggregate crime pattern analysis for public safety research |
| KalkiDharma | Government spending and governance transparency analysis |
| KalkiSamaj | Social development indicator tracking and gap analysis |
| KalkiVayu | Environmental monitoring and public health correlation |
| KalkiArtha | Economic indicator analysis and trend forecasting |

- Data acquired for one module **cannot be repurposed** for another module without Ethics Board review
- Purpose documentation is maintained in `ETHICS.md` and in each module's README
- Any change in purpose requires community review and updated documentation

### 2.4 Cross-Border Data Processing

DPDPA restricts the transfer of personal data to jurisdictions that the Central Government may designate as restricted.

- **Kalki policy**: all data processing occurs on **Indian infrastructure**
- Contributors outside India work with anonymized, aggregated datasets only — never with raw or potentially re-identifiable data
- No personal data is stored on international servers, cloud platforms, or CDNs outside India
- If cloud infrastructure is used, it must be hosted in Indian data center regions

### 2.5 Kalki's Compliance Approach

Kalki takes a **defense-in-depth** approach to DPDPA compliance:

1. **Aggregation**: all outputs are at aggregate level — minimum group sizes enforced (see `ETHICS.md` Section 3)
2. **k-Anonymity**: minimum group size of 100 individuals for any output
3. **No personal data storage**: only statistical aggregates and anonymized records persist
4. **Purpose-bound processing**: documented purpose for each module and data source
5. **Regular compliance audits**: Ethics Board conducts quarterly reviews
6. **Privacy Impact Assessments**: required before any new data pipeline is deployed

---

## 3. RTI Act, 2005 — Right to Information

The Right to Information Act, 2005 is a powerful tool for Indian citizens to obtain information from public authorities. It is a legitimate and valuable channel for acquiring data that Kalki needs for analysis.

### 3.1 Using RTI for Data Acquisition

- RTI empowers any Indian citizen to request information held by public authorities
- RTI data supplements officially published datasets and fills gaps in publicly available information
- RTI requests can be filed for specific datasets, reports, or records that are not otherwise published
- Government departments are obligated to respond within 30 days (or 48 hours for matters involving life and liberty)

### 3.2 Filing RTI Requests for Kalki

**Process**:

1. **Identify data need**: determine what data is required and which public authority holds it
2. **Check existing sources**: verify the data is not already available through data.gov.in, departmental websites, or published reports
3. **Draft RTI request**: use templates maintained in `docs/rti-templates/`
4. **File request**: via rtionline.gov.in (online) or by post to the Public Information Officer (PIO) of the relevant authority
5. **Track response**: log the request in the project issue tracker with RTI reference number
6. **Process response**: anonymize and aggregate as per standard data handling procedures

**Community coordination**:

- Maintain a shared tracker to avoid duplicate RTI requests
- Coordinate across contributors to ensure systematic data acquisition
- Share learnings about effective RTI strategies

### 3.3 Limitations

- **Redistribution restrictions**: RTI responses may come with implicit or explicit restrictions on redistribution — always verify before publishing raw RTI data
- **Section 8 exemptions**: certain information is exempt from RTI disclosure, including:
  - Information affecting sovereignty, security, or strategic interests (8(1)(a))
  - Information that would cause breach of privilege of Parliament/Legislature (8(1)(c))
  - Commercial confidence, trade secrets, intellectual property (8(1)(d))
  - Information available to a person in fiduciary relationship (8(1)(e))
  - Personal information with no public interest relationship (8(1)(j))
- **Data quality**: RTI data should be cross-verified against other sources where possible
- **Attribution**: always cite RTI responses with the reference number, date, and responding authority

---

## 4. IT Act, 2000 — Information Technology Act

The Information Technology Act, 2000 (and subsequent amendments) governs cyber activities in India. Several provisions are relevant to Kalki's operations.

### 4.1 Section 69A — Government Blocking Powers

Section 69A empowers the Central Government to direct intermediaries to block public access to information in the interest of sovereignty, security, public order, or other specified grounds.

- **Awareness**: Kalki's platform and data could potentially be subject to blocking orders
- **Recommendations**:
  - Maintain **data mirrors** in geographically distributed locations within India
  - **Archive critical datasets** with content-addressed storage (IPFS hashes, SHA-256 checksums) for integrity verification
  - Document any blocking orders received and seek legal counsel immediately
  - Maintain transparent communication with the community about any government directions received
- **Compliance**: Kalki will comply with lawful orders while pursuing all available legal remedies

### 4.2 Section 43A — Data Protection Obligations

Section 43A (read with the Information Technology (Reasonable Security Practices and Procedures and Sensitive Personal Data or Information) Rules, 2011) imposes data protection obligations on bodies corporate handling sensitive personal data.

- **Kalki's approach**: avoid handling sensitive personal data entirely
- If sensitive personal data is inadvertently collected, it must be:
  1. Identified immediately through automated detection
  2. Quarantined from all processing pipelines
  3. Deleted within 24 hours
  4. Documented in the incident log
- Contributors must report any suspected exposure of sensitive personal data immediately

### 4.3 Responsible Disclosure

If contributors discover security vulnerabilities in government portals or systems during legitimate data collection activities:

1. **Do NOT exploit** the vulnerability — do not access any data beyond what is publicly available
2. **Document** the finding with screenshots, timestamps, and technical details
3. **Report** to CERT-In (Indian Computer Emergency Response Team) within **24 hours**:
   - Email: incident@cert-in.org.in
   - Website: cert-in.org.in
4. **Do not publicly disclose** until the vulnerability is patched or **90 days** have elapsed since reporting
5. **Never** use a discovered vulnerability to access non-public data, even for Kalki's purposes
6. Maintain records of all disclosures made

> **Note**: Responsible disclosure protects both the contributor and the public. Exploiting vulnerabilities — even with good intentions — can result in criminal liability under the IT Act.

---

## 5. Government Data Copyright

### 5.1 Government Works in India

Unlike the United States (where federal government works are in the public domain), **Indian government works are copyrighted** under the Copyright Act, 1957.

- Copyright in government works vests in the Government of India
- Government publications are protected for **60 years** from the date of first publication
- This means government data, reports, and publications **cannot be freely reproduced** without permission or a legal basis
- This is a significant consideration for any project that processes government data

### 5.2 Fair Dealing — Section 52

Section 52 of the Copyright Act, 1957 provides exceptions to copyright infringement, including fair dealing:

- **Section 52(1)(a)**: fair dealing with a work for the purposes of:
  - Private or personal use, including research
  - Criticism or review
- Kalki's use case — public interest research and analysis — likely qualifies as fair dealing
- **Best practices**:
  - **Transform** data: analyze, aggregate, visualize — rather than republishing raw government datasets
  - **Attribute** the source clearly in all outputs
  - Add **analytical value**: Kalki outputs should be substantially different from source data
  - Avoid bulk reproduction of government publications without transformation

### 5.3 Open Government License — India (OGL-India)

- Some government data is explicitly published under the **Open Government License — India** (primarily through data.gov.in)
- OGL-India permits:
  - Reproduction and adaptation
  - Commercial and non-commercial use
  - Redistribution
- **Requirements**: attribution to the source department and data.gov.in
- **Verify individually**: not all government data is OGL-licensed — check each dataset's license terms

### 5.4 Navigating Copyright Claims

When government portals claim restrictive copyright or terms:

- **Prefer officially open datasets**: data.gov.in and OGL-licensed sources
- **Use official APIs** where provided — API terms often permit analytical use
- **For restricted data**: cite the source, link to the original, and analyze — avoid bulk reproduction
- **Document copyright status**: maintain copyright and license status for each data source in `DATA_SOURCES.md`
- **Seek clarification**: when copyright terms are ambiguous, contact the data publisher for clarification
- **Legal review**: for critical datasets with unclear copyright, seek legal opinion before integration

---

## 6. Terms of Use Compliance

### 6.1 Government Portal ToS

Many government portals include Terms of Service (ToS) or Terms of Use that govern how their data can be accessed and used.

- Some portals explicitly **prohibit automated access** (web scraping, bots)
- Some restrict use to **personal, non-commercial purposes**
- Violations of ToS could expose contributors to legal risk, even if the underlying data is public
- ToS restrictions should be taken seriously — they represent the data publisher's conditions of access

### 6.2 Kalki's Approach

Kalki follows a **preference hierarchy** for data access, prioritizing low-risk methods:

| Priority | Data Access Method | Risk Level | Notes |
|---|---|---|---|
| 1 | Official APIs | Low | Preferred — designed for programmatic access |
| 2 | Bulk data downloads (data.gov.in) | Low | Pre-packaged for reuse |
| 3 | OGL-licensed datasets | Low | Explicitly open for reuse |
| 4 | RTI requests | Low | Legal right of citizens |
| 5 | Manual data collection | Medium | Labor-intensive but legally safe |
| 6 | Automated scraping | **High** | Last resort — requires legal review |

**Principles**:

- Each data source's ToS is reviewed and documented in `DATA_SOURCES.md`
- Automated scraping is used **only as a last resort** and only after:
  - Legal review of the portal's ToS
  - Assessment of legal risk
  - Ethics Board notification
- Respect `robots.txt` directives and implement rate limiting
- Cache data locally to minimize load on source servers
- Identify Kalki's user agent honestly — do not impersonate browsers or other software

---

## 7. Licensing

### 7.1 Source Code — AGPL-3.0

All Kalki source code is licensed under the **GNU Affero General Public License v3.0** (AGPL-3.0).

**Why AGPL-3.0**:

- **Prevents proprietary surveillance forks**: any entity that modifies Kalki and deploys it must share their modifications under the same license
- **Network copyleft**: unlike GPL, AGPL extends copyleft to network use — even deploying Kalki as a web service triggers the obligation to share source code
- **Ethical safeguard**: makes it legally difficult for bad actors to take Kalki's code, modify it for surveillance purposes, and deploy it without transparency
- **Community benefit**: ensures all improvements flow back to the community

**Obligations for users and deployers**:

- Provide complete corresponding source code to all users of the deployed service
- Preserve all copyright notices and license headers
- Clearly indicate any modifications made
- License derivative works under AGPL-3.0

### 7.2 Processed Datasets

Kalki-generated datasets (aggregated outputs, visualizations, analytical results) are published under:

- **OGL-India** (Open Government License — India) for datasets derived primarily from Indian government sources
- **CC-BY-4.0** (Creative Commons Attribution 4.0 International) for all other datasets

**Requirements**:

- Attribution: "Generated by Kalki — India's Open Intelligence Platform"
- Datasets include metadata documenting: processing methodology, source data references, date of generation, and applicable caveats
- License terms are embedded in dataset metadata

### 7.3 Documentation

All Kalki documentation (including this document) is licensed under **CC-BY-SA-4.0** (Creative Commons Attribution-ShareAlike 4.0 International).

- Contributors grant this license upon contribution
- Third-party content is cited with its original license preserved
- Share-alike provision ensures documentation improvements remain open

### 7.4 License Compatibility

| Component | License | Copyleft Type | Commercial Use |
|---|---|---|---|
| Source code | AGPL-3.0 | Strong (network) | Yes, with source sharing |
| Processed datasets | OGL-India / CC-BY-4.0 | None | Yes, with attribution |
| Documentation | CC-BY-SA-4.0 | Share-alike | Yes, with attribution |
| Third-party dependencies | Varies | Check individually | Verify compatibility |

**Dependency policy**:

- All third-party dependencies must be license-compatible with AGPL-3.0
- Dependencies with restrictive licenses (proprietary, SSPL, BUSL) are not permitted
- License compatibility is verified during code review
- A dependency license audit is conducted quarterly

---

## 8. Liability Limitation

### 8.1 Decision Support, Not Decisions

> **Kalki outputs are decision-support tools. They are NOT decisions, verdicts, findings of fact, or official determinations of any kind.**

- Outputs are analytical indicators based on publicly available data
- They reflect the limitations, biases, and gaps inherent in source data
- No guarantee of accuracy, completeness, timeliness, or fitness for any particular purpose
- Users must **independently verify** information before taking any action based on Kalki outputs

### 8.2 No Warranty

Kalki is provided **"as is"** and **"as available"** without warranty of any kind, either express or implied, including but not limited to:

- Warranties of accuracy or reliability
- Warranties of fitness for a particular purpose
- Warranties of non-infringement
- Warranties of uninterrupted or error-free operation

Contributors and maintainers are not liable for errors, omissions, or inaccuracies in outputs, or for any actions taken in reliance on those outputs.

### 8.3 Prohibited Uses

> **Any use of Kalki outputs for enforcement, persecution, discrimination, or targeting of individuals or communities is expressly prohibited. Such use violates this document, the Kalki Ethics Framework, and the Kalki Code of Conduct.**

Specific prohibited uses include:

- Using outputs to justify enforcement action, arrest, or prosecution of individuals
- Using outputs to discriminate against communities, castes, religions, or regions
- Representing Kalki outputs as official government findings, legal evidence, or judicial determinations
- Redistributing Kalki outputs without the accompanying context, methodology notes, and disclaimers
- Using Kalki outputs in any system that makes automated decisions affecting individuals
- Presenting Kalki's analytical indicators as established facts in media, legal proceedings, or policy documents without appropriate qualification

### 8.4 Indemnification

- Users and deployers agree to indemnify Kalki contributors and maintainers against any claims, damages, or liabilities arising from misuse of Kalki tools, data, or outputs
- Contributors acting in good faith within the ethical framework and project guidelines are protected by the project's indemnification commitment
- This indemnification does not extend to contributors who knowingly violate the Ethics Framework or applicable law

---

*This document is maintained by the Kalki Core Team. It is reviewed quarterly and updated as Indian law evolves. For legal questions, open a discussion on GitHub or contact the Core Team.*

*Last updated: May 2026 | Version: 1.0 | License: CC-BY-SA-4.0*
