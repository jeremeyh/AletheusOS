"""Canonical models for Living Constitutional Instrumentation™."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def new_instrument_signal_id() -> str:
    return (
        "INSTRUMENT-SIGNAL-"
        f"{uuid4().hex[:12].upper()}"
    )


class InstrumentKind(StrEnum):
    GAUGE = "gauge"
    METER = "meter"
    PULSE = "pulse"
    SPECTRUM = "spectrum"
    CONSENSUS = "consensus"
    CONFIDENCE = "confidence"
    TRUTH = "truth"
    RADAR = "radar"
    TIMELINE = "timeline"
    TREND = "trend"
    INDICATOR = "indicator"
    DIGITAL_READOUT = "digital_readout"


class InstrumentSignalType(StrEnum):
    VALUE_CHANGED = "value_changed"
    ACTIVITY_STARTED = "activity_started"
    ACTIVITY_COMPLETED = "activity_completed"
    ACTIVITY_FAILED = "activity_failed"
    CONFIDENCE_CHANGED = "confidence_changed"
    CONVERGENCE_CHANGED = "convergence_changed"
    DISSENT_CHANGED = "dissent_changed"
    VIRTUE_STATE_CHANGED = "virtue_state_changed"
    HEALTH_CHANGED = "health_changed"
    EVIDENCE_CHANGED = "evidence_changed"
    TIMELINE_EVENT = "timeline_event"


class InstrumentStatus(StrEnum):
    IDLE = "idle"
    ACTIVE = "active"
    STABLE = "stable"
    CAUTION = "caution"
    CONTESTED = "contested"
    DEGRADED = "degraded"
    FAILED = "failed"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class InstrumentDefinition:
    """
    Semantic definition of one constitutional instrument.

    Definitions describe what an instrument means. They do not dictate its
    visual implementation.
    """

    instrument_id: str
    canonical_name: str
    kind: InstrumentKind
    signal_source: str

    minimum: float = 0.0
    maximum: float = 1.0
    unit: str = ""

    description: str = ""
    constitutional_meaning: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        if not self.instrument_id.strip():
            raise ValueError(
                "instrument_id may not be blank."
            )

        if not self.canonical_name.strip():
            raise ValueError(
                "canonical_name may not be blank."
            )

        if self.maximum <= self.minimum:
            raise ValueError(
                "Instrument maximum must be greater "
                "than minimum."
            )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["kind"] = self.kind.value
        return value


@dataclass(frozen=True, slots=True)
class InstrumentSignal:
    """One semantically meaningful instrumentation update."""

    instrument_id: str
    signal_type: InstrumentSignalType
    source_identity: str

    value: float | None = None
    status: InstrumentStatus | None = None
    confidence: float | None = None

    cognition_id: str | None = None
    correlation_id: str | None = None

    message: str = ""
    payload: dict[str, Any] = field(
        default_factory=dict
    )

    signal_id: str = field(
        default_factory=new_instrument_signal_id
    )
    emitted_at: str = field(
        default_factory=utc_now
    )

    def __post_init__(self) -> None:
        if not self.instrument_id.strip():
            raise ValueError(
                "instrument_id may not be blank."
            )

        if not self.source_identity.strip():
            raise ValueError(
                "source_identity may not be blank."
            )

        if (
            self.confidence is not None
            and not 0.0 <= self.confidence <= 1.0
        ):
            raise ValueError(
                "Signal confidence must be between "
                "0.0 and 1.0."
            )

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["signal_type"] = (
            self.signal_type.value
        )
        value["status"] = (
            self.status.value
            if self.status is not None
            else None
        )
        return value


@dataclass(frozen=True, slots=True)
class InstrumentState:
    """Read-only projected state of one constitutional instrument."""

    instrument_id: str
    canonical_name: str
    kind: InstrumentKind

    current_value: float | None
    minimum: float
    maximum: float
    unit: str

    status: InstrumentStatus
    confidence: float | None

    update_count: int
    last_signal_id: str | None
    last_updated: str | None
    last_message: str

    history: tuple[InstrumentSignal, ...]
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def normalized_value(self) -> float | None:
        if self.current_value is None:
            return None

        span = self.maximum - self.minimum

        value = (
            self.current_value - self.minimum
        ) / span

        return round(
            min(1.0, max(0.0, value)),
            4,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "instrument_id": self.instrument_id,
            "canonical_name": self.canonical_name,
            "kind": self.kind.value,
            "current_value": self.current_value,
            "normalized_value": (
                self.normalized_value
            ),
            "minimum": self.minimum,
            "maximum": self.maximum,
            "unit": self.unit,
            "status": self.status.value,
            "confidence": self.confidence,
            "update_count": self.update_count,
            "last_signal_id": self.last_signal_id,
            "last_updated": self.last_updated,
            "last_message": self.last_message,
            "history": [
                signal.to_dict()
                for signal in self.history
            ],
            "metadata": dict(self.metadata),
        }
