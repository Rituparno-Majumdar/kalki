"""
Kalki schema package.

Defines the canonical data models that all connectors, analytics modules,
and API layers must use. Every record flowing through Kalki must conform
to the types defined here.

Primary types:
    KalkiLocation   — India administrative hierarchy (state → village)
    KalkiRecord     — raw data record output by a connector
    KalkiSignal     — processed analytical signal output by a module
    KalkiBriefing   — natural-language intelligence output (Intelligence Layer)
"""

from schema.models import (
    KalkiBriefing,
    KalkiLocation,
    KalkiRecord,
    KalkiSignal,
    Module,
    SignalSeverity,
    SignalType,
)

__all__ = [
    "KalkiBriefing",
    "KalkiLocation",
    "KalkiRecord",
    "KalkiSignal",
    "Module",
    "SignalSeverity",
    "SignalType",
]
