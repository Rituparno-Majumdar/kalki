"""
BaseConnector: the interface every Kalki data connector must implement.

To build a connector for a new data source:
1. Create a new directory under connectors/ (e.g. connectors/imd/)
2. Create your connector class inheriting from BaseConnector
3. Implement all abstract methods
4. See connectors/example_connector.py for a fully-annotated example

Connector contract:
- fetch()              → downloads raw data from the source
- validate(raw)        → checks the raw data is usable; returns issues list
- to_standard_schema() → transforms raw data into KalkiRecord list
- get_metadata()       → describes the connector for the registry

All connectors must satisfy these guarantees:
- Public data only: no authentication that implies private data access
- Full provenance: raw source preserved, transformation logged
- Idempotent: running the connector twice with the same data produces
  the same output (no duplicate records)
- Quality scoring: every record carries a data_quality_score (0.0–1.0)
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core data types
# ---------------------------------------------------------------------------

class Module(str, Enum):
    PRAKRITI = "kalki_prakriti"   # Climate & Disaster
    SHIKSHA  = "kalki_shiksha"    # Education
    SWASTHA  = "kalki_swastha"    # Health & Epidemiology
    ARTHA    = "kalki_artha"      # Economic Stress
    NAGRIK   = "kalki_nagrik"     # Civic Infrastructure
    SAMAJ    = "kalki_samaj"      # Social & Demographic
    DHARMA   = "kalki_dharma"     # Governance & Transparency
    CRIME    = "kalki_crime"      # Crime Patterns (build last)


@dataclass
class KalkiLocation:
    """India administrative hierarchy for a data record."""
    state: str
    district: str
    block: str | None = None
    village: str | None = None

    # ISO 3166-2 state code where known (e.g. "IN-OD" for Odisha)
    state_code: str | None = None
    # LGD district code (Govt of India Local Government Directory)
    district_lgd_code: str | None = None


@dataclass
class KalkiRecord:
    """
    The standard output unit for every Kalki connector.

    Every connector's to_standard_schema() must return a list of these.
    """
    # Who produced this record
    source_name: str              # e.g. "IMD District Weather"
    source_url: str               # exact URL the data was fetched from
    connector_version: str        # semver of the connector (e.g. "0.1.0")
    module: Module

    # Where and when
    location: KalkiLocation
    record_timestamp: datetime    # the time the *data* refers to
    fetch_timestamp: datetime     # the time the connector fetched it

    # The data payload — free-form dict; schema defined per connector
    data: dict[str, Any]

    # Data quality score: composite 0.0–1.0 (see ARCHITECTURE.md)
    # Completeness 30% + Timeliness 25% + Consistency 20% +
    # Accuracy 15% + Provenance 10%
    data_quality_score: float = 0.0

    # Raw source preserved for audit trail (never discard)
    raw_source_hash: str | None = None   # SHA-256 of the raw document


@dataclass
class ConnectorMetadata:
    """Describes a connector for the registry and contributor guide."""
    name: str                      # e.g. "IMD District Weather Connector"
    source_name: str               # e.g. "India Meteorological Department"
    source_url: str                # base URL of the data source
    module: Module
    version: str                   # semver
    maintainer: str | None = None  # GitHub username
    update_frequency: str = ""     # e.g. "daily", "monthly", "real-time"
    data_format: str = ""          # e.g. "JSON API", "CSV bulk", "HTML scrape"
    # Known limitations or caveats about this source
    caveats: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    """Returned by validate(). Connector should not proceed if is_valid=False."""
    is_valid: bool
    issues: list[str] = field(default_factory=list)   # human-readable problems
    warnings: list[str] = field(default_factory=list) # non-blocking concerns


# ---------------------------------------------------------------------------
# Abstract base class
# ---------------------------------------------------------------------------

class BaseConnector(ABC):
    """
    Abstract base class for all Kalki data connectors.

    Subclass this and implement the four abstract methods. The run()
    method orchestrates the full fetch → validate → transform pipeline.
    """

    @abstractmethod
    def get_metadata(self) -> ConnectorMetadata:
        """
        Return static metadata describing this connector.

        Called by the connector registry to self-document the source.
        Must not make any network calls.
        """
        ...

    @abstractmethod
    def fetch(self) -> Any:
        """
        Download raw data from the source.

        - Use requests, httpx, or playwright for HTTP sources.
        - Use tabula-py / camelot for PDF sources.
        - Store the raw response; do not transform here.
        - Raise ConnectorFetchError on unrecoverable fetch failures.

        Returns:
            Raw data in whatever form the source provides
            (bytes, str, dict, DataFrame, etc.).
        """
        ...

    @abstractmethod
    def validate(self, raw: Any) -> ValidationResult:
        """
        Check that raw data is usable before transformation.

        Typical checks:
        - Expected fields are present
        - Date ranges are plausible
        - No obvious encoding issues
        - Row count is within expected bounds

        This method must NOT raise exceptions — capture issues in
        ValidationResult.issues instead.

        Returns:
            ValidationResult with is_valid=True/False and issue list.
        """
        ...

    @abstractmethod
    def to_standard_schema(self, raw: Any) -> list[KalkiRecord]:
        """
        Transform raw data into a list of KalkiRecord instances.

        Rules:
        - One KalkiRecord per atomic observation (e.g. one district × one day)
        - Compute data_quality_score for every record
        - Preserve raw_source_hash (SHA-256 of the raw document)
        - Never drop records silently — log at WARNING level instead
        - Location codes must use LGD district codes where available

        Returns:
            List of KalkiRecord; may be empty if no valid records found.
        """
        ...

    # -------------------------------------------------------------------
    # Orchestration — do not override unless you have a good reason
    # -------------------------------------------------------------------

    def run(self) -> list[KalkiRecord]:
        """
        Full pipeline: fetch → validate → transform.

        Override individual steps (fetch, validate, to_standard_schema)
        rather than this method.
        """
        meta = self.get_metadata()
        logger.info("Running connector: %s v%s", meta.name, meta.version)

        raw = self.fetch()
        logger.debug("Fetch complete for %s", meta.source_name)

        result = self.validate(raw)
        if not result.is_valid:
            logger.error(
                "Validation failed for %s: %s",
                meta.source_name,
                "; ".join(result.issues),
            )
            return []

        for warning in result.warnings:
            logger.warning("Connector %s: %s", meta.name, warning)

        records = self.to_standard_schema(raw)
        logger.info(
            "Connector %s produced %d records", meta.name, len(records)
        )
        return records


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ConnectorFetchError(Exception):
    """Raised when a connector cannot retrieve data from its source."""


class ConnectorValidationError(Exception):
    """Raised when a connector encounters an unrecoverable schema mismatch."""
