"""Configuration for SPAN™."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class SPANConfig:
    """Runtime configuration for SPAN™.

    The defaults intentionally favor advisory behavior. SPAN may analyze,
    navigate, and recommend, but it must not mutate platform state directly.
    """

    capability_name: str = "span"
    capability_version: str = "1.0.0"
    advisory_only: bool = True
    minimum_recommendation_confidence: float = 0.70
    maximum_evidence_age: timedelta = timedelta(days=30)
    require_constitutional_assessment: bool = True
    enable_strategic_memory: bool = True
    enabled_spartan_domains: tuple[str, ...] = field(
        default_factory=lambda: (
            "spatial",
            "platform",
            "runtime",
            "architecture",
            "capability",
            "knowledge",
            "governance",
            "standards",
            "research",
            "technology",
            "innovation",
            "forecasting",
            "evolution",
            "constitutional",
            "security",
        )
    )

    def validate(self) -> None:
        if not 0.0 <= self.minimum_recommendation_confidence <= 1.0:
            raise ValueError(
                "minimum_recommendation_confidence must be between 0.0 and 1.0"
            )
        if self.maximum_evidence_age.total_seconds() <= 0:
            raise ValueError("maximum_evidence_age must be positive")
        if not self.capability_name.strip():
            raise ValueError("capability_name must not be empty")
        if not self.capability_version.strip():
            raise ValueError("capability_version must not be empty")
