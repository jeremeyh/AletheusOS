"""Canonical models for the AletheusOS Institution Framework."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class ConstitutionalPillar(StrEnum):
    """The four permanent Foundation Pillars."""

    INTENT = "intent"
    INTELLIGENCE = "intelligence"
    GOVERNANCE = "governance"
    MEMORY = "memory"


class ConstitutionalLayer(StrEnum):
    """High-level constitutional placement of an institution."""

    FOUNDATION = "foundation"
    GOVERNANCE = "governance"
    RUNTIME = "runtime"
    INTELLIGENCE = "intelligence"
    MEMORY = "memory"
    EXPERIENCE = "experience"
    PERSISTENCE = "persistence"
    SECURITY = "security"
    INTEGRATION = "integration"
    APPLICATION = "application"
    CROSS_CUTTING = "cross_cutting"


class InstitutionStatus(StrEnum):
    """Lifecycle state of an institutional definition."""

    PROPOSED = "proposed"
    CONSTITUTIONAL = "constitutional"
    ENGINEERING = "engineering"
    IMPLEMENTED = "implemented"
    DEPRECATED = "deprecated"
    HISTORICAL = "historical"


class InstitutionCriticality(StrEnum):
    """Operational significance of an institution."""

    SUPPORTING = "supporting"
    IMPORTANT = "important"
    CRITICAL = "critical"
    CONSTITUTIONAL = "constitutional"


@dataclass(frozen=True, slots=True)
class InstitutionRecord:
    """
    Canonical identity and constitutional contract for one institution.

    An InstitutionRecord describes what a permanent AletheusOS institution
    is. It does not implement the institution's runtime behavior.
    """

    institution_id: str
    canonical_name: str
    purpose: str
    authority: str
    jurisdiction: str
    constitutional_layer: ConstitutionalLayer
    pillar: ConstitutionalPillar

    status: InstitutionStatus = InstitutionStatus.ENGINEERING
    criticality: InstitutionCriticality = InstitutionCriticality.IMPORTANT

    responsibilities: tuple[str, ...] = ()
    non_responsibilities: tuple[str, ...] = ()

    consumes: tuple[str, ...] = ()
    produces: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()

    observed_by: tuple[str, ...] = ()
    governed_by: tuple[str, ...] = ()
    certified_by: tuple[str, ...] = ()

    repository_locations: tuple[str, ...] = ()
    ontology_tags: tuple[str, ...] = ()
    constitutional_articles: tuple[str, ...] = ()

    genesis: str = "unknown"
    version: str = "0.1.0"
    owner: str = "AletheusOS"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-compatible representation."""

        value = asdict(self)
        value["constitutional_layer"] = self.constitutional_layer.value
        value["pillar"] = self.pillar.value
        value["status"] = self.status.value
        value["criticality"] = self.criticality.value
        return value
