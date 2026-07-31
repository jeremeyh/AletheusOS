"""Canonical Constitutional Mission definitions."""

from __future__ import annotations

from .models import (
    ConstitutionalMission,
    MissionContract,
    MissionCriticality,
    new_mission_id,
)

SECURITY_CONTAINMENT_CONTRACT = MissionContract(
    mission_type="security_containment",
    purpose=(
        "Classify, contain, preserve evidence of, and stabilize "
        "a constitutional security incident."
    ),
    required_institutions=(
        "aletheus.watch_tower",
        "aletheus.guardian",
        "aletheus.conclave",
        "aletheus.containment_vault",
        "aletheus.sentinel",
    ),
    required_evidence_types=(
        "integrity_finding",
        "threat_classification",
        "containment_result",
        "forensic_preservation",
        "stabilization_result",
    ),
    success_criteria=(
        "Threat was classified.",
        "Entity was quarantined.",
        "Forensic evidence was preserved.",
        "Runtime incident was stabilized.",
    ),
    failure_criteria=(
        "Threat classification failed.",
        "Containment failed.",
        "Evidence preservation failed.",
        "Runtime stabilization failed.",
    ),
    governance_required=True,
)


def create_security_containment_mission(
    *,
    entity_id: str,
    severity: str,
) -> ConstitutionalMission:
    mission_id = new_mission_id()

    return ConstitutionalMission(
        mission_id=mission_id,
        mission_type=(SECURITY_CONTAINMENT_CONTRACT.mission_type),
        canonical_name="Security Containment Mission™",
        purpose=SECURITY_CONTAINMENT_CONTRACT.purpose,
        authority="Security Civilization™",
        jurisdiction="Constitutional security containment",
        contract=SECURITY_CONTAINMENT_CONTRACT,
        criticality=MissionCriticality.CONSTITUTIONAL,
        correlation_id=mission_id,
        metadata={
            "entity_id": entity_id,
            "severity": severity,
        },
    )
