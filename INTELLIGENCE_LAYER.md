# Intelligence Layer

> **"A dashboard shows you what happened. An intelligence system tells you what it means and what to do next."**

---

## Why This Layer Exists

The rest of the Kalki architecture — connectors, data lake, analytics engine — produces **structured signals**: numbers, scores, anomaly flags. These are necessary but not sufficient. A district collector looking at a flood risk score of 0.78 still has to ask: *Is that bad? Compared to what? What should I actually do?*

The Intelligence Layer answers those questions. It takes the structured outputs of the Analytics & ML Engine and synthesises them into **natural-language intelligence briefings** — actionable, sourced, confidence-aware summaries written for a specific audience.

This is what separates Kalki from a dashboard.

---

## Architecture Overview

```
ANALYTICS & ML ENGINE
(structured signals: scores, anomalies, forecasts)
        │
        ▼
┌──────────────────────────────────────────────────┐
│              INTELLIGENCE LAYER                  │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Tier 1: Data Extraction LLM             │   │
│  │  (inside Ingestion Layer)                │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Tier 2: Intelligence Synthesis LLM      │   │  ← Core innovation
│  │  (new layer, between Analytics & API)    │   │
│  └──────────────────────────────────────────┘   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │  Tier 3: Query Interface LLM             │   │
│  │  (on top of API Gateway)                 │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
        │
        ▼
  HUMAN REVIEW QUEUE
  (required before publication — ETHICS.md)
        │
        ▼
  API GATEWAY → DASHBOARD
```

---

## Tier 1 — Data Extraction LLM

**Where it sits:** Inside the existing Ingestion & Cleaning Layer.

**The problem it solves:** Indian government data is the hardest engineering challenge in the entire Kalki pipeline. Rule-based parsers fail regularly on:

- PDFs where column headers are in Hindi, data in English
- Schema drift — the same dataset published with different column names year-to-year
- Tables embedded in scanned images
- Multi-language headers with Unicode inconsistencies
- Footnotes that modify the meaning of table cells

LLMs handle these cases far more reliably than regex or `tabula-py` alone.

**How it works:**

```
Input:  raw document (PDF, HTML, CSV) + target schema definition
Output: structured JSON matching KalkiRecord schema
        + extraction confidence score (0.0–1.0)
        + list of fields that could not be extracted
```

Every extraction logs:
- The raw source (preserved in data lake — never discarded)
- The prompt used
- The model response
- The confidence score

**When to use Tier 1 vs rule-based parsers:**

| Source type | Recommended approach |
|---|---|
| Clean JSON/REST API | Rule-based (no LLM needed) |
| Consistent CSV bulk download | Rule-based |
| HTML table, consistent schema | Rule-based with fallback to Tier 1 |
| PDF with known layout | `tabula-py` with Tier 1 fallback |
| PDF with variable layout | Tier 1 |
| Scanned document / image table | OCR + Tier 1 |
| Schema changes year-to-year | Tier 1 with schema-mapping prompt |

**Why build this first:** It improves data quality for every downstream layer immediately, and it solves the highest-stated risk in the existing documentation.

---

## Tier 2 — Intelligence Synthesis LLM

**Where it sits:** New layer inserted between the Analytics & ML Engine and the API Gateway.

**What it produces:** `KalkiBriefing` objects (defined in `schema/models.py`). Each briefing is a synthesised intelligence assessment for a specific audience.

### Briefing Output Format

Every briefing must follow this structure — enforced via JSON schema before prose generation:

```json
{
  "situation_summary": "2–3 sentence overview of the current situation",
  "evidence": [
    {
      "label": "IMD Rainfall Forecast",
      "value": "180% of normal for the next 7 days",
      "source_signal_id": "<uuid>",
      "confidence": 0.91
    }
  ],
  "recommended_actions": [
    "Pre-position relief supplies in Ganjam and Puri districts within 72 hours",
    "Activate NDRF team standby in Bhubaneswar"
  ],
  "data_limitations": [
    "NDMA preparedness data is 6 weeks old — current readiness may differ",
    "No river gauge data available for 3 of 12 affected blocks"
  ]
}
```

### Audience Types

The recommended actions and framing change by audience. The same underlying signals produce different briefings for:

| Audience | Framing | Action language |
|---|---|---|
| `district_collector` | Operational, urgent | "Pre-position", "Activate", "Deploy" |
| `journalist` | Explanatory, contextual | "Data shows", "Compared to last year", "Experts say" |
| `researcher` | Technical, hedged | Confidence intervals, methodology notes |
| `public` | Plain language, accessible | "What this means for you", "What to do if..." |

### The Non-Negotiable Design Principle: Grounded Generation Only

The LLM **cannot assert anything that does not trace to a specific signal** in the analytical store. Every claim in a briefing must cite a `source_signal_id`. Freeform speculation is not permitted.

This is both an engineering constraint and an ethics requirement. Journalists and government officials will fact-check outputs. One fabricated statistic destroys the project's credibility permanently.

Implementation: the LLM is given structured signal data as input and asked to generate the briefing JSON. It is explicitly instructed that every evidence item must reference a provided signal ID. The output is then validated — if any evidence item references a non-existent signal ID, the briefing is rejected and returned to the queue.

### Human Review Before Publication

All Tier 2 briefings enter a review queue with status `PENDING` before any external publication. A human reviewer (initially the project founder; later a module maintainer) sets status to:

- `APPROVED` — publish via API and dashboard
- `REJECTED` — not suitable; add reviewer notes
- `ESCALATED` — refer to Ethics Board (triggers when `demographic_flag=True` on any source signal)

This is operationally feasible because Kalki publishes analysis, not real-time alerts. The review cadence is daily or weekly per module — not continuous.

---

## Tier 3 — Query Interface LLM

**Where it sits:** On top of the API Gateway, as an optional interface layer.

**What it does:** Natural-language querying of historical data and predictions.

```
User:    "Show me flood risk trends for Odisha's coastal districts
          over the last 3 monsoon seasons"

         ↓  LLM translates to structured query

System:  GET /api/signals?module=kalki_prakriti
                         &signal_type=risk_score
                         &state=Odisha
                         &period_start=2022-06-01
                         &period_end=2025-10-01

         ↓  Returns data + auto-generated chart description
```

**Build this last.** It is high-value for journalists and researchers but depends on Tiers 1 and 2 being operational first. A query interface on an empty database is useless.

---

## India-Specific Grounding Requirements

For Tier 2 briefings to be correct and useful, the LLM must be grounded in India-specific context that its training data alone cannot be trusted to provide accurately. This grounding is loaded as context at inference time — pulled from Kalki's own analytical store (DuckDB), not from model memory.

| Context | Why it matters | Source |
|---|---|---|
| Administrative hierarchy (State → District → Block → Village) | Geographic scope of every prediction | Ontology layer + LGD codes |
| Monsoon calendar (onset/withdrawal dates by region) | Climate signals only make sense relative to seasonal norms | IMD historical data |
| Kharif / Rabi agricultural calendar | Crop and economic signals need seasonal framing | AgMarkNet data |
| Governance structures (NDMA, NHM, state equivalents) | Recommended actions must name the correct agency | Static reference data |
| District-level baselines (historical flood frequency, health infrastructure capacity, poverty index) | Anomaly detection requires knowing what "normal" is | Census, NDMA, HMIS data |
| Correct district name spellings | LLMs have inconsistent spellings for Indian district names | LGD canonical name list |

**Implementation:** A system prompt template is maintained per module. At inference time, the relevant district baselines and seasonal context are retrieved from DuckDB and injected into the prompt. The LLM never relies on its training data for India-specific facts.

---

## Hallucination Mitigation

Confident-sounding incorrect outputs are the highest-risk failure mode for Kalki. A wrong statistic published under Kalki's name — especially one that reaches a journalist or government official — causes irreversible credibility damage.

Four mitigations in sequence:

### 1. Structured Output First
The LLM outputs JSON matching a strict schema. Prose is generated from validated JSON — not freeform text. If the JSON is invalid or references a non-existent signal ID, the generation is rejected before it reaches a human reviewer.

### 2. Citation Verification
After generation, an automated check confirms:
- Every `source_signal_id` in the evidence list exists in the analytical store
- The cited value matches the actual signal value (within a defined tolerance)
- The location referenced in the briefing matches the signals' locations

Any mismatch → briefing rejected, logged for investigation.

### 3. Confidence Floor
Briefings with `overall_confidence` below **0.6** do not reach the human review queue. They are stored in a separate `low_confidence` queue for later investigation or discarding.

The `overall_confidence` is computed as the weighted average of the evidence item confidences, penalised for data staleness and coverage gaps.

### 4. Human Review
The final net. No briefing is published without a human approval. This is already required by `ETHICS.md` (human-in-the-loop principle) and is the backstop for anything the automated checks miss.

---

## Model Selection

The Intelligence Layer is designed to be **model-agnostic**. Any LLM with the following capabilities can drive Tier 2:

- Structured JSON output (enforced schema)
- Context window of at least 32k tokens (to accommodate multi-signal input)
- Reliable instruction-following for grounded generation constraints

Suitable options include hosted API models (proprietary or open) and self-hosted open-source models (Llama 3, Mistral, Qwen). For contributors building or testing the Intelligence Layer locally, a self-hosted model via Ollama is a zero-cost option.

**Sovereignty consideration:** For government adoption, a self-hosted open-source model on Indian infrastructure is strongly preferable to a foreign-hosted API. Design the Tier 2 interface so the model provider is swappable without changing the surrounding code.

```python
# The model call is isolated behind a single interface
class IntelligenceLLM(ABC):
    @abstractmethod
    def generate_briefing(self, signals: list[KalkiSignal], audience: str) -> dict:
        ...

# Implementations: OpenAIIntelligenceLLM, OllamaIntelligenceLLM, etc.
```

---

## Integration With Existing Architecture

The Intelligence Layer adds one new box to the architecture diagram in `ARCHITECTURE.md`:

```
┌───────────────────────────────────────────────────────────────────────┐
│                     ANALYTICS & ML ENGINE                             │
│  Pattern Detection · Anomaly Scoring · Forecasting · Bias Detection  │
└──────────────────────────────┬────────────────────────────────────────┘
                               ▼
┌───────────────────────────────────────────────────────────────────────┐  ← NEW
│                      INTELLIGENCE LAYER                               │
│  Tier 2: LLM Synthesis · Grounded Generation · Confidence Scoring    │
│  Briefing JSON Schema · Citation Verification · Human Review Queue   │
└──────────────┬───────────────────────────────────┬────────────────────┘
               ▼                                   ▼
┌──────────────────────────┐          ┌─────────────────────────────────┐
│    ALERTING ENGINE       │          │     API GATEWAY                 │
│  Threshold-based alerts  │          │     REST + GraphQL (+ Tier 3)   │
└──────────────────────────┘          └─────────────────────────────────┘
```

And Tier 1 is noted as an addition to the Ingestion Layer:

```
┌───────────────────────────────────────────────────────────────────────┐
│                    INGESTION & CLEANING LAYER                         │
│  Scrapers · API Connectors · PDF Parsers · OCR · Schema Normalizer   │
│  + Tier 1: LLM-assisted extraction for complex/inconsistent sources  │  ← NOTE
└───────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Roadmap

Build in this order — each tier depends on the previous:

| Tier | Depends on | When to build |
|---|---|---|
| **Tier 1** (data extraction) | At least 1 connector with messy source data | As soon as first complex connector hits extraction failures |
| **Tier 2** (synthesis) | `KalkiSignal` records in the database | After the analytics engine produces its first signals |
| **Tier 3** (query interface) | Working API Gateway | After Phase 2 API gateway is live |

Do not build Tier 2 before there are real signals to synthesise. A synthesis layer with no data to synthesise produces nothing useful and is hard to test.

---

## Open Issues

The following are not yet resolved and should be decided by the community before implementation:

- **Review queue UI:** Where does the human reviewer see and approve briefings? A simple admin panel, a Slack integration, or something else?
- **Briefing storage:** Are approved briefings served directly from Postgres, or cached in a CDN?
- **Tier 1 cost management:** LLM API calls per document can be expensive at scale. At what document volume does a local self-hosted model become preferable?
- **Multi-language briefings:** Tier 2 briefings should eventually be generated in Hindi, Tamil, Bengali, and other languages. Does translation happen at the LLM generation step or as a post-processing step?
