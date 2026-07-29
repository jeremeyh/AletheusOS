from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class HealthEvidence:

    source: str

    healthy: bool

    category: str

    message: str

    metadata: dict = field(
        default_factory=dict
    )


@dataclass(frozen=True, slots=True)
class RuntimeHealth:

    healthy: bool

    evidence: tuple[HealthEvidence,...]

    timestamp: str
