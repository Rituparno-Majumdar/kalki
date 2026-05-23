# Contributing to Kalki

> **Building India's Open Intelligence Platform — together.**

Welcome, and thank you for considering contributing to Kalki! 🙏

Kalki is an ambitious project: an open-source, community-driven intelligence and forecasting platform built for Indian public interest. We're building something that doesn't exist yet — a transparent system that helps India's citizens, researchers, journalists, and policymakers understand what's really happening across the country.

We can't do this alone. Kalki needs **data engineers**, **ML researchers**, **frontend developers**, **domain experts**, **translators**, **testers**, and **curious minds** who care about India's future. Whether you have 2 hours on a weekend or 20 hours a week, there's meaningful work waiting for you.

This guide will help you get started.

---

## Ways to Contribute

Contributions are listed below in order of **priority** and **accessibility**. If you're not sure where to start, begin at the top.

---

### 🔌 Data Connectors — *Highest Priority*

**This is the single most impactful way to contribute to Kalki.**

Every insight Kalki produces begins with data. Data connectors are modular components that fetch, clean, validate, and score data from Indian government and public data sources. Each connector handles **one data source** and follows a standard interface:

```
fetch → clean → quality_score → validate
```

**Why start here?**
- A connector is a self-contained unit — you can build one **in a weekend**
- You don't need to understand the full system architecture
- Every new connector immediately expands what Kalki can analyze
- There are dozens of Indian government data sources waiting to be connected

**Where they live:** `connectors/<source_name>/`

**Examples of data sources that need connectors:**
- data.gov.in datasets (agriculture, infrastructure, health)
- India Meteorological Department (IMD) weather data
- NCRB crime statistics
- Election Commission results data
- Air quality monitoring (CPCB)
- Census and demographic data
- Parliamentary question answers and proceedings

> 💡 **New to the project? Start here.** Pick a data source you're familiar with, build a connector, and you'll have a complete, merged contribution in days — not months.

---

### 📊 Data Quality and Cleaning

Indian government data is messy. Really messy. Help us make it usable.

- Improve existing connectors' cleaning logic
- Handle edge cases: Hindi/Devanagari text normalization, malformed dates, encoding issues (UTF-8 vs legacy encodings)
- Build shared cleaning utilities in `utils/cleaning/`
- Develop data quality scoring algorithms
- Create validation rules for common Indian data formats (Aadhaar masking, IFSC codes, PIN codes, state/district name normalization)

---

### 🧠 Analytics and Models

Build the intelligence layer that turns data into insight.

- **Pattern detection** — algorithms that surface meaningful trends across datasets
- **Anomaly scoring** — models that flag unusual patterns for human review
- **Forecasting** — time-series models for economic, environmental, and social indicators
- **Bias detection** — frameworks that identify and quantify bias in data and model outputs
- **Cross-source correlation** — methods to link signals across disparate datasets

> Requires background in ML, data science, or statistics. Familiarity with Indian data contexts is a significant plus.

---

### 🗺️ Dashboard and Visualization

Make Kalki's intelligence accessible and understandable.

- **India map visualizations** — state and district-level choropleth maps
- **District drill-down views** — interactive exploration from national → state → district
- **Chart components** — reusable, accessible chart components for common visualizations
- **Responsive mobile design** — Kalki must work on the devices India actually uses
- **Accessibility** — screen reader support, high contrast modes, keyboard navigation

> Requires frontend skills: React/Next.js, D3.js, Leaflet/Mapbox. Design contributions (Figma mockups, UX research) are equally welcome.

---

### 📖 Documentation

Great documentation makes the difference between a project that grows and one that stalls.

- **Translations** — Help us reach India's diverse developer community
  - Hindi, Tamil, Bengali, Telugu, Kannada, Malayalam, Marathi, Gujarati, and more
  - Priority: README, CONTRIBUTING guide, and Getting Started tutorial
- **Tutorials and guides** — Step-by-step walkthroughs for common tasks
- **Data source documentation** — Document quirks, update schedules, and access methods for Indian data sources
- **Architecture documentation** — Improve and maintain technical architecture docs
- **API documentation** — Keep endpoint documentation current and clear

---

### 🔍 Domain Research

You don't need to write code to make Kalki smarter.

- **Identify new data sources** — Find and document publicly available Indian government datasets
- **Document data source quirks** — Update schedules, format changes, access restrictions, historical availability
- **Signal identification** — What patterns in the data are actually meaningful? What's noise?
- **Ethics review** — Help evaluate whether specific data uses align with Kalki's ethical principles
- **Comparative research** — How do similar platforms work in other countries? What can we learn?

---

### 🐛 Bug Reports and Testing

Quality is not optional when people rely on your data.

- **Report data quality issues** — Spotted bad data? File an issue with evidence
- **Test connectors against live sources** — Government websites change without notice; help us catch breakage early
- **Performance testing** — Profile connectors and analytics pipelines for bottlenecks
- **Edge case testing** — Test with unusual inputs, large datasets, and boundary conditions
- **CI/CD improvements** — Help us catch problems before they reach main

---

## Getting Started

### Step 1: Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/<your-username>/kalki.git
cd kalki
```

### Step 2: Set Up Your Development Environment

**Prerequisites:**
- Python 3.11 or higher
- Docker and Docker Compose
- Node.js 18+ (for dashboard development)
- Git

**Environment setup:**

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Start infrastructure services
docker-compose up -d

# Verify your setup
python -m pytest tests/ --quick
```

### Step 3: Find Your First Task

1. Browse the [Issue Tracker](../../issues) for labels:
   - `good-first-issue` — Scoped tasks ideal for newcomers
   - `help-wanted` — Tasks where maintainers need community help
   - `connector-needed` — Data sources waiting for a connector
   - `documentation` — Writing and translation tasks
2. Comment on the issue to let others know you're working on it
3. Ask questions! No question is too basic — use GitHub Discussions or Discord

### Step 4: Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b connector/data-source-name
```

### Step 5: Build, Test, and Submit

```bash
# Run tests
python -m pytest tests/

# Check code style
flake8 .
mypy .

# Push and open a PR
git push origin your-branch-name
```

---

## Building a Data Connector — Quick Guide

This is the most common contribution path. Here's how to build a connector from scratch.

### Connector Directory Structure

```
connectors/
└── your_source_name/
    ├── __init__.py
    ├── connector.py        # Main connector class
    ├── cleaner.py          # Data cleaning logic
    ├── config.py           # Source-specific configuration
    ├── schemas.py          # Data schemas and validation
    ├── tests/
    │   ├── __init__.py
    │   ├── test_connector.py
    │   ├── test_cleaner.py
    │   └── fixtures/       # Sample data for testing
    │       └── sample_response.json
    └── README.md           # Data source documentation
```

### Step-by-Step Walkthrough

**1. Create your connector class by extending `BaseConnector`:**

```python
from kalki.connectors.base import BaseConnector
from kalki.models import DataPackage, QualityScore

class YourSourceConnector(BaseConnector):
    """Connector for [Your Data Source Name].
    
    Source: https://data.gov.in/resource/...
    Update frequency: Monthly
    Coverage: National / State-level
    """

    SOURCE_ID = "your_source_name"
    SOURCE_URL = "https://api.data.gov.in/..."
    UPDATE_FREQUENCY = "monthly"

    def fetch(self) -> dict:
        """Fetch raw data from the source API or website."""
        # Implement HTTP requests, pagination, error handling
        ...

    def clean(self, raw_data: dict) -> list[dict]:
        """Transform raw data into standardized format."""
        # Normalize dates, clean text, standardize names
        ...

    def quality_score(self, cleaned_data: list[dict]) -> QualityScore:
        """Assess the quality of the fetched data."""
        # Check completeness, freshness, consistency
        ...

    def validate(self, cleaned_data: list[dict]) -> bool:
        """Validate cleaned data against the expected schema."""
        # Schema validation, type checks, range checks
        ...
```

**2. Implement the cleaning logic in `cleaner.py`:**

Handle the realities of Indian government data — mixed-language text, inconsistent date formats (`DD/MM/YYYY`, `DD-MM-YY`, Hindi dates), state name variations, and encoding issues.

**3. Write tests:**

```python
def test_fetch_returns_data(connector, mock_api):
    """Verify fetch retrieves data successfully."""
    result = connector.fetch()
    assert result is not None
    assert len(result) > 0

def test_clean_normalizes_dates(connector, sample_data):
    """Verify date normalization handles Indian formats."""
    cleaned = connector.clean(sample_data)
    for record in cleaned:
        assert record["date"].format == "YYYY-MM-DD"

def test_quality_score_reflects_completeness(connector, partial_data):
    """Verify quality scoring detects missing fields."""
    score = connector.quality_score(partial_data)
    assert score.completeness < 1.0
```

**4. Document your connector** in its `README.md`:
- What data source does it connect to?
- What data does it return?
- How often is the source updated?
- Any known quirks or limitations?
- How to get API keys (if required)

**5. Include sample output** — Add a representative sample of cleaned output in `tests/fixtures/` so reviewers can see what the connector produces.

---

## Code Standards

### Python

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines
- Use **type hints** on all function signatures
- Write **docstrings** for all public classes and functions (Google style)
- Format with `black` and lint with `flake8`
- Type check with `mypy` (strict mode for connectors)

### JavaScript / TypeScript

- Follow the project ESLint configuration
- Format with Prettier
- Use TypeScript for all new dashboard code
- Prefer functional components and hooks (React)

### Testing

- **Python:** pytest
- **JavaScript:** Jest + React Testing Library
- **Minimum test coverage:** 80% for connectors, 70% for other modules
- All tests must pass in CI before merge
- Include both unit tests and integration tests for connectors

### General

- Commit messages: use [Conventional Commits](https://www.conventionalcommits.org/) format
  - `feat(connector): add IMD weather data connector`
  - `fix(cleaner): handle UTF-8 encoding in NCRB data`
  - `docs: translate getting started guide to Hindi`
- Keep PRs focused — one logical change per PR
- No secrets, API keys, or credentials in code (use environment variables)

---

## Pull Request Process

### Before Submitting

- [ ] Your code follows the project's code standards
- [ ] You've added or updated tests for your changes
- [ ] All existing tests pass locally (`python -m pytest tests/`)
- [ ] You've updated relevant documentation
- [ ] For connectors: you've included sample output in `tests/fixtures/`

### Submitting Your PR

1. **Write a descriptive title** using Conventional Commits format
2. **Fill out the PR template** with:
   - What this PR does and why
   - How to test the changes
   - Screenshots (for UI changes)
   - Sample output (for connectors)
3. **Link to the relevant issue(s)** using `Closes #123` or `Relates to #456`

### Review Process

1. **Automated CI** runs tests, linting, and type checking
2. **At least one module maintainer** must approve the PR
3. **For new data sources**, the Ethics Board reviews the data source appropriateness
4. Maintainers may request changes — this is normal and constructive
5. Once approved and CI passes, a maintainer will merge your PR

### After Merge

- Your contribution is now part of Kalki! 🎉
- You'll be added to CONTRIBUTORS.md
- If this is your first contribution, welcome to the community!

---

## Contributor Levels

Kalki recognizes contributors through a transparent progression path:

| Level | Badge | How to Reach | Privileges |
|---|---|---|---|
| **Contributor** | 🌱 | Submit 1 merged PR | Listed in CONTRIBUTORS.md |
| **Regular Contributor** | 🌿 | 5+ merged PRs | Invited to contributor Discord, early access to roadmap discussions |
| **Reviewer** | 🌳 | Nominated by maintainers for consistent, high-quality reviews | Can approve PRs in their module |
| **Module Maintainer** | 🏔️ | Nominated by Core Team for domain expertise and sustained contribution | Owns module roadmap, merge access within module, speaks at community calls |
| **Core Team** | ⭐ | Invited by Founder + existing Core Team | Cross-module merge access, release management, governance participation |

> **Progression is based on quality, consistency, and community trust — not just volume.** A contributor who writes thoughtful reviews and helps newcomers may progress faster than one who submits many low-context PRs.

---

## Communication

### GitHub Discussions

Our primary forum for technical discussions, proposals, and questions. Use the appropriate category:
- **Ideas** — Propose new features, data sources, or approaches
- **Q&A** — Ask questions about the codebase, architecture, or contributing
- **Show & Tell** — Share what you've built with Kalki
- **RFC** — Formal proposals for significant changes

### Discord

Real-time chat for the Kalki community. Join us at: *[Discord invite link — coming soon]*

Channels include `#general`, `#connectors`, `#analytics`, `#dashboard`, `#help`, and module-specific channels.

### Monthly Community Calls

On the **last Saturday of each month**, we hold an open community call:
- **Demo Day** — Contributors showcase recent work
- **Roadmap Discussion** — What's coming next and where help is needed
- **Open Floor** — Questions, ideas, and feedback from anyone

Meeting links and recordings are posted in GitHub Discussions.

### Issue Tracker

Use GitHub Issues for:
- 🐛 **Bug reports** — Something broken? Tell us
- ✨ **Feature requests** — What should Kalki do next?
- 📡 **Data source proposals** — Know a public dataset we should connect to?

---

## Recognition

Every contribution matters, and we make sure contributors are recognized:

- **All contributors** are listed in [CONTRIBUTORS.md](CONTRIBUTORS.md) with their contribution areas
- **Module maintainers** are credited in their module's README
- **Regular contributors** are highlighted in monthly community updates
- **Significant contributions** are featured in release notes
- **Conference talks and blog posts** about Kalki always credit the community

---

## Code of Conduct

Kalki is committed to providing a welcoming, inclusive, and harassment-free experience for everyone. All contributors are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md).

**In brief:** Be respectful. Be constructive. Be inclusive. Assume good intentions.

If you experience or witness unacceptable behavior, please report it to the Core Team at *[conduct email — coming soon]*.

---

## Questions?

- **Stuck on setup?** Open a Q&A discussion on GitHub Discussions
- **Not sure where to contribute?** Look for `good-first-issue` labels or ask in Discord
- **Have an idea?** Open an Ideas discussion — we'd love to hear it
- **Want to propose a new data source?** File a Data Source Proposal issue

---

> *"The best time to plant a tree was twenty years ago. The second best time is now."*
>
> India's open intelligence platform starts with your first contribution. We're glad you're here.
