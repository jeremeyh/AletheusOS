"""Canonical Constitutional Case definitions."""

from __future__ import annotations

from .models import (
    CaseContract,
    CaseCriticality,
    CaseSeverity,
    ConstitutionalCase,
    new_case_id,
)

SECURITY_INCIDENT_CASE_CONTRACT = CaseContract(
    case_type="security_incident",
    purpose=(
        "Preserve the complete constitutional context of a "
        "security incident across one or more missions."
    ),
    permitted_mission_types=(
        "security_containment",
        "security_recovery",
        "security_verification",
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
    closure_criteria=(
        "Threat was classified.",
        "Affected entity was contained.",
        "Evidence was preserved.",
        "Runtime was stabilized.",
        "Resolution was independently verified.",
    ),
    governance_required=True,
)


def create_security_incident_case(
    *,
    entity_id: str,
    severity: CaseSeverity | str,
) -> ConstitutionalCase:
    case_id = new_case_id()

    resolved_severity = (
        severity
        if isinstance(severity, CaseSeverity)
        else CaseSeverity(severity)
    )

    return ConstitutionalCase(
        case_id=case_id,
        case_type=SECURITY_INCIDENT_CASE_CONTRACT.case_type,
        canonical_name="Security Incident Case™",
        purpose=SECURITY_INCIDENT_CASE_CONTRACT.purpose,
        authority="Security Civilization™",
        jurisdiction="Constitutional security incidents",
        contract=SECURITY_INCIDENT_CASE_CONTRACT,
        severity=resolved_severity,
        criticality=CaseCriticality.CONSTITUTIONAL,
        correlation_id=case_id,
        metadata={
            "entity_id": entity_id,
        },
    )
