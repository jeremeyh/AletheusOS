from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Literal


HealthState = Literal[
    "healthy",
    "degraded",
    "unavailable",
    "unknown",
]

MissionState = Literal[
    "planned",
    "active",
    "blocked",
    "complete",
]

ConfidenceLabel = Literal[
    "unknown",
    "low",
    "moderate",
    "high",
    "verified",
]


@dataclass(frozen=True, slots=True)
class ExperienceConfidence:
    value: float
    label: ConfidenceLabel
    basis: str | None = None

    def __post_init__(self) -> None:
        if not 0 <= self.value <= 1:
            raise ValueError(
                "Confidence value must be between 0 and 1."
            )


@dataclass(frozen=True, slots=True)
class ExperienceProvenance:
    source_id: str
    source_type: str
    label: str
    observed_at: str | None = None


@dataclass(frozen=True, slots=True)
class ExperienceUncertainty:
    known: bool
    description: str
    material: bool


@dataclass(frozen=True, slots=True)
class ExperienceReversibility:
    reversible: bool
    undo_label: str | None = None
    consequence: str | None = None


@dataclass(frozen=True, slots=True)
class PrincipleXEnvelope:
    state: str
    explanation: str
    reversibility: ExperienceReversibility
    confidence: ExperienceConfidence | None = None
    provenance: tuple[ExperienceProvenance, ...] = ()
    uncertainty: tuple[ExperienceUncertainty, ...] = ()

    def __post_init__(self) -> None:
        if not self.state.strip():
            raise ValueError(
                "Principle X state cannot be empty."
            )

        if not self.explanation.strip():
            raise ValueError(
                "Principle X explanation cannot be empty."
            )


@dataclass(frozen=True, slots=True)
class ExperienceHealthCheck:
    id: str
    name: str
    state: HealthState
    detail: str
    checked_at: str
    latency_ms: int | None = None


@dataclass(frozen=True, slots=True)
class ExperienceHealthSnapshot:
    state: HealthState
    summary: str
    passing_checks: int
    total_checks: int
    warning_count: int
    checks: tuple[ExperienceHealthCheck, ...]
    truth: PrincipleXEnvelope

    def __post_init__(self) -> None:
        if self.passing_checks < 0:
            raise ValueError(
                "passing_checks cannot be negative."
            )

        if self.total_checks < 0:
            raise ValueError(
                "total_checks cannot be negative."
            )

        if self.passing_checks > self.total_checks:
            raise ValueError(
                "passing_checks cannot exceed total_checks."
            )

        if self.warning_count < 0:
            raise ValueError(
                "warning_count cannot be negative."
            )


@dataclass(frozen=True, slots=True)
class ExperienceMission:
    id: str
    name: str
    description: str
    state: MissionState
    progress: int
    confidence: ExperienceConfidence | None = None
    provenance: tuple[ExperienceProvenance, ...] = ()
    uncertainty: tuple[ExperienceUncertainty, ...] = ()

    def __post_init__(self) -> None:
        if not 0 <= self.progress <= 100:
            raise ValueError(
                "Mission progress must be between 0 and 100."
            )


@dataclass(frozen=True, slots=True)
class ExperienceOverview:
    health: ExperienceHealthSnapshot
    missions: tuple[ExperienceMission, ...]
    generated_at: str


@dataclass(frozen=True, slots=True)
class ExperienceResponse:
    data: Any
    generated_at: str
    request_id: str
    schema_version: str = "0.1.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return _serialize(asdict(self))


def _serialize(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            _camel_case(str(key)): _serialize(child)
            for key, child in value.items()
        }

    if isinstance(value, list):
        return [
            _serialize(child)
            for child in value
        ]

    if isinstance(value, tuple):
        return [
            _serialize(child)
            for child in value
        ]

    return value


def _camel_case(value: str) -> str:
    head, *tail = value.split("_")
    return head + "".join(
        part[:1].upper() + part[1:]
        for part in tail
    )
