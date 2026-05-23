"""
Kalki canonical data models.

These are the core types that flow through the entire Kalki platform:

    Raw data (connectors)
        └─► KalkiRecord        one observation from one source
              └─► KalkiSignal  one processed analytical signal
                    └─► KalkiBriefing  synthesised intelligence output

All connector output must be expressed as KalkiRecord instances.
All module (analytics) output must be expressed as KalkiSignal instances.

Types use Python dataclasses (stdlib, no extra dependencies). Pydantic
validation will be layered on top once a requirements.txt is established.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class Module(str, Enum):
    """The eight Kalki domain modules, in build priority order."""
    PRAKRITI = "kalki_prakriti"   # 1 — Climate & Disaster (MVP)
    SHIKSHA  = "kalki_shiksha"    # 2 — Education
    SWASTHA  = "kalki_swastha"    # 3 — Health & Epidemiology
    ARTHA    = "kalki_artha"      # 4 — Economic Stress
    NAGRIK   = "kalki_nagrik"     # 5 — Civic Infrastructure
    SAMAJ    = "kalki_samaj"      # 6 — Social & Demographic
    DHARMA   = "kalki_dharma"     # 7 — Governance & Transparency
    CRIME    = "kalki_crime"      # 8 — Crime Patterns (build last)


class SignalType(str, Enum):
    """
    The category of analytical signal a module can emit.

    RISK_SCORE      — a normalised 0.0–1.0 risk or stress index
    ANOMALY         — a statistical deviation from historical baseline
    FORECAST        — a forward-looking estimate (with confidence interval)
    GAP             — a measured shortfall against a target or benchmark
    CORRELATION     — a detected relationship between two or more variables
    TREND           — a directional change over time (up/down/flat)
    ALERT           — a threshold breach requiring immediate attention
    """
    RISK_SCORE  = "risk_score"
    ANOMALY     = "anomaly"
    FORECAST    = "forecast"
    GAP         = "gap"
    CORRELATION = "correlation"
    TREND       = "trend"
    ALERT       = "alert"


class SignalSeverity(str, Enum):
    """
    Human-interpretable severity of a KalkiSignal.
    Used for dashboard colouring and alert routing.
    """
    INFO     = "info"      # background monitoring, no action needed
    LOW      = "low"       # worth watching
    MEDIUM   = "medium"    # warrants attention
    HIGH     = "high"      # requires action
    CRITICAL = "critical"  # immediate response recommended


# ---------------------------------------------------------------------------
# Location — India administrative hierarchy
# ---------------------------------------------------------------------------

@dataclass
class KalkiLocation:
    """
    Represents a geographic entity within India's administrative hierarchy:
        State → District → Block → Village / Ward

    All Kalki data is anchored to a KalkiLocation. Granularity depends on
    the data source: most sources are district-level; some are block-level.

    Code standards:
        state_code       ISO 3166-2 subdivision code, e.g. "IN-OD" (Odisha)
        district_lgd_code  Local Government Directory district code (preferred
                           over free-text names for joins and deduplication)

    See: https://lgdirectory.gov.in/
    """
    state: str
    district: str
    block: str | None = None
    village: str | None = None
    ward: str | None = None          # for urban local bodies

    state_code: str | None = None            # ISO 3166-2, e.g. "IN-OD"
    district_lgd_code: str | None = None     # LGD district code, e.g. "373"
    block_lgd_code: str | None = None

    # Latitude / longitude centroid — populated from the Kalki ontology layer
    latitude: float | None = None
    longitude: float | None = None


# ---------------------------------------------------------------------------
# KalkiRecord — raw data unit output by a connector
# ---------------------------------------------------------------------------

@dataclass
class KalkiRecord:
    """
    The atomic output unit of a data connector.

    One KalkiRecord represents a single observation: one location, one
    time period, one source. Connectors produce lists of these.

    Every field here is mandatory for the audit trail and data lineage
    requirements in ETHICS.md. Do not omit source_url or raw_source_hash.

    data_quality_score (0.0–1.0) is a composite of five dimensions:
        Completeness  30%
        Timeliness    25%
        Consistency   20%
        Accuracy      15%
        Provenance    10%
    See ARCHITECTURE.md § Data Quality Scoring for the full formula.
    """
    # Provenance
    source_name: str          # human-readable source name
    source_url: str           # exact URL the raw data was fetched from
    connector_version: str    # semver of the connector that produced this

    # Classification
    module: Module

    # Spatiotemporal
    location: KalkiLocation
    record_timestamp: datetime    # the time the *data* refers to
    fetch_timestamp: datetime     # when the connector fetched it

    # Payload — domain-specific dict; schema defined per connector
    data: dict[str, Any]

    # Quality
    data_quality_score: float = 0.0   # 0.0 = unusable, 1.0 = perfect

    # Audit trail — SHA-256 of the raw document before transformation
    raw_source_hash: str | None = None


# ---------------------------------------------------------------------------
# KalkiSignal — processed analytical output from a module
# ---------------------------------------------------------------------------

@dataclass
class KalkiSignal:
    """
    A single analytical signal produced by a Kalki module.

    Signals are the output of the Analytics & ML Engine. They represent
    a processed insight derived from one or more KalkiRecords.

    Ethics requirements (ETHICS.md):
    - All signals are aggregate-level (min. 100 individuals where applicable)
    - Individual-level signals are prohibited
    - Every signal must be traceable to its source records (source_record_ids)
    - Signals with demographic correlations must set demographic_flag=True
      and must not be published without Ethics Board review

    confidence (0.0–1.0): the model's confidence in this signal.
    Signals below 0.6 confidence should not be published externally.
    """
    # Identity
    signal_id: str              # UUID generated at creation time
    module: Module
    signal_type: SignalType
    severity: SignalSeverity

    # Spatiotemporal scope
    location: KalkiLocation
    period_start: datetime
    period_end: datetime

    # The signal value — interpretation depends on signal_type:
    #   RISK_SCORE:   float 0.0–1.0
    #   ANOMALY:      z-score (float, may be negative)
    #   FORECAST:     dict with "value", "lower_bound", "upper_bound"
    #   GAP:          dict with "actual", "target", "gap_pct"
    #   CORRELATION:  dict with "variable_a", "variable_b", "r", "p_value"
    #   TREND:        dict with "direction", "magnitude", "period"
    #   ALERT:        dict with "threshold", "observed", "metric"
    value: Any

    # Confidence in this signal (0.0–1.0). Do not publish below 0.6.
    confidence: float

    # Traceability — IDs of the KalkiRecords that produced this signal
    source_record_ids: list[str] = field(default_factory=list)

    # Human-readable one-line description of what the signal means
    label: str = ""

    # Ethics flags
    # Set True if the signal correlates with caste, religion, or gender
    # demographics (r > 0.3). Blocks publication until Ethics Board reviews.
    demographic_flag: bool = False

    # Aggregation — must be ≥ 100 where individuals are counted
    population_count: int | None = None

    # Model metadata
    model_name: str | None = None
    model_version: str | None = None
    generated_at: datetime | None = None


# ---------------------------------------------------------------------------
# KalkiBriefing — Intelligence Layer output
# ---------------------------------------------------------------------------

@dataclass
class KalkiBriefingItem:
    """A single evidence point within a KalkiBriefing."""
    label: str                    # short description, e.g. "IMD Rainfall Forecast"
    value: str                    # formatted value, e.g. "180% of normal"
    source_signal_id: str         # ID of the KalkiSignal this comes from
    confidence: float


@dataclass
class KalkiBriefing:
    """
    A synthesised intelligence briefing produced by the Intelligence Layer.

    Briefings are natural-language summaries that synthesise multiple
    KalkiSignals into an actionable assessment for a specific audience.

    All briefings require human review before external publication.
    The review_status field tracks this:
        PENDING   — awaiting human reviewer
        APPROVED  — cleared for publication
        REJECTED  — not suitable for publication (reason in reviewer_notes)
        ESCALATED — referred to Ethics Board

    Output format aligns with INTELLIGENCE_LAYER.md specification.
    """

    class ReviewStatus(str, Enum):
        PENDING   = "pending"
        APPROVED  = "approved"
        REJECTED  = "rejected"
        ESCALATED = "escalated"

    # Identity
    briefing_id: str
    module: Module

    # Scope
    location: KalkiLocation
    period_start: datetime
    period_end: datetime

    # Audience — determines language and recommended-actions framing
    # e.g. "journalist", "district_collector", "researcher", "public"
    audience: str

    # Content
    situation_summary: str           # 2–3 sentence overview
    evidence: list[KalkiBriefingItem] = field(default_factory=list)
    recommended_actions: list[str]   = field(default_factory=list)
    data_limitations: list[str]      = field(default_factory=list)

    # Overall confidence (0.0–1.0). Do not publish below 0.6.
    overall_confidence: float = 0.0

    # Source signals this briefing synthesises
    source_signal_ids: list[str] = field(default_factory=list)

    # Review workflow (human-in-the-loop, required by ETHICS.md)
    review_status: ReviewStatus = ReviewStatus.PENDING
    reviewer: str | None = None
    reviewer_notes: str | None = None

    generated_at: datetime | None = None
    published_at: datetime | None = None
