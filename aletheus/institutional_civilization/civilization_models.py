"""Canonical civilization models for AletheusOS."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any


class CivilizationStatus(StrEnum):
    PROPOSED = "proposed"
    CONSTITUTIONAL = "constitutional"
    ENGINEERING = "engineering"
    OPERATIONAL = "operational"
    DEPRECATED = "deprecated"
    HISTORICAL = "historical"


class CivilizationCriticality(StrEnum):
    SUPPORTING = "supporting"
    IMPORTANT = "important"
    CRITICAL = "critical"
    CONSTITUTIONAL = "constitutional"


@dataclass(frozen=True, slots=True)
class CivilizationRecord:
    """
    Canonical constitutional domain containing related institutions.

    A Civilization does not replace its member institutions. It defines
    their shared constitutional domain, purpose, governing boundaries,
    and cross-institutional coherence.
    """

    civilization_id: str
    canonical_name: str
    purpose: str
    authority_domain: str

    institution_ids: tuple[str, ...]
    responsibilities: tuple[str, ...]
    non_responsibilities: tuple[str, ...]

    governed_by: tuple[str, ...] = ()
    observed_by: tuple[str, ...] = ()
    collaborates_with: tuple[str, ...] = ()

    status: CivilizationStatus = CivilizationStatus.ENGINEERING
    criticality: CivilizationCriticality = (
        CivilizationCriticality.CRITICAL
    )

    constitutional_articles: tuple[str, ...] = ()
    ontology_tags: tuple[str, ...] = ()
    genesis: str = "12"
    version: str = "0.1.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["status"] = self.status.value
        value["criticality"] = self.criticality.value
        return value
