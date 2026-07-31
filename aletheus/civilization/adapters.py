"""Domain adapters used by the Civilization Orchestrator."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from aletheus.constitutional_events import ConstitutionalEvent


@dataclass(frozen=True, slots=True)
class EvidenceProjection:
    evidence_type: str
    source_identity: str
    evidence: dict[str, Any]


class SecurityCivilizationAdapter:
    """
    Maps Security Civilization events into canonical Mission and Case evidence.

    The adapter contains domain knowledge so the Orchestrator remains
    independent of Guardian, Conclave, Sentinel, and Vault implementation.
    """

    EVENT_EVIDENCE_MAP = {
        "IntegrityFindingCreated": "integrity_finding",
        "ThreatClassified": "threat_classification",
        "EntityQuarantined": "containment_result",
        "EvidencePreserved": "forensic_preservation",
        "SecurityIncidentStabilized": "stabilization_result",
    }

    def evidence_from_events(
        self,
        events: tuple[ConstitutionalEvent, ...],
    ) -> tuple[EvidenceProjection, ...]:
        projections = []

        for event in events:
            event_name = event.event_type.value
            evidence_type = self.EVENT_EVIDENCE_MAP.get(event_name)

            if evidence_type is None:
                continue

            projections.append(
                EvidenceProjection(
                    evidence_type=evidence_type,
                    source_identity=event.source_identity,
                    evidence={
                        "event_id": event.event_id,
                        "event_type": event_name,
                        "effective_at": event.effective_at,
                        "payload": dict(event.payload),
                        "evidence": list(event.evidence),
                        "certified": event.certified,
                    },
                )
            )

        return tuple(projections)

    def validate_complete(
        self,
        projections: tuple[EvidenceProjection, ...],
        required_evidence_types: tuple[str, ...],
    ) -> None:
        projected_types = {projection.evidence_type for projection in projections}

        missing = set(required_evidence_types) - projected_types

        if missing:
            raise ValueError(
                "Security response did not produce required evidence: "
                + ", ".join(sorted(missing))
            )
