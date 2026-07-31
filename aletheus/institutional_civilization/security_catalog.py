"""Canonical security institutions for AletheusOS."""

from __future__ import annotations

from .models import (
    ConstitutionalLayer,
    ConstitutionalPillar,
    InstitutionCriticality,
    InstitutionRecord,
    InstitutionStatus,
)


def canonical_security_institutions() -> tuple[InstitutionRecord, ...]:
    """Return canonical security institutions."""

    return (
        InstitutionRecord(
            institution_id="aletheus.guardian",
            canonical_name="Guardian™",
            purpose=(
                "Coordinate defensive reasoning, threat classification, "
                "response strategy, and constitutional protection."
            ),
            authority="Coordinated constitutional defense",
            jurisdiction="Platform defense coordination",
            constitutional_layer=ConstitutionalLayer.GOVERNANCE,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Receive integrity and security findings.",
                "Classify threats.",
                "Coordinate defensive strategy.",
                "Escalate containment requests.",
            ),
            non_responsibilities=(
                "Perform repository discovery.",
                "Replace Council governance.",
                "Contain entities directly.",
            ),
            dependencies=(
                "aletheus.watch_tower",
                "aletheus.sentinel",
            ),
            consumes=(
                "integrity_findings",
                "runtime_security_signals",
                "risk_assessments",
            ),
            produces=(
                "threat_classifications",
                "containment_requests",
                "governance_escalations",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            certified_by=("aletheus.council",),
            repository_locations=(
                "aletheus/runtime/guardian",
                "reports/guardian",
            ),
            ontology_tags=(
                "security",
                "defense",
                "classification",
            ),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.conclave",
            canonical_name="Conclave™",
            purpose=(
                "Provide constitutional containment, trust-boundary "
                "enforcement, and secure isolation."
            ),
            authority="Containment authority",
            jurisdiction="Security containment",
            constitutional_layer=ConstitutionalLayer.SECURITY,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Contain suspicious entities.",
                "Enforce trust boundaries.",
                "Coordinate secure release.",
            ),
            non_responsibilities=(
                "Perform threat discovery.",
                "Replace Guardian.",
                "Destroy evidence.",
            ),
            dependencies=(
                "aletheus.guardian",
                "aletheus.containment_vault",
            ),
            consumes=(
                "containment_requests",
                "threat_classifications",
            ),
            produces=(
                "containment_actions",
                "quarantine_requests",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.sentinel",
                "aletheus.homeostasis",
            ),
            certified_by=("aletheus.council",),
            repository_locations=(
                "aletheus/runtime/conclave",
                "reports/conclave",
            ),
            ontology_tags=(
                "security",
                "containment",
                "isolation",
            ),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.containment_vault",
            canonical_name="Containment Vault™",
            purpose=(
                "Persist quarantined entities, forensic evidence, "
                "snapshots, and chain-of-custody history."
            ),
            authority="Quarantine persistence",
            jurisdiction="Security evidence",
            constitutional_layer=ConstitutionalLayer.PERSISTENCE,
            pillar=ConstitutionalPillar.MEMORY,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Store quarantined assets.",
                "Preserve forensic evidence.",
                "Maintain chain of custody.",
            ),
            non_responsibilities=(
                "Classify threats.",
                "Authorize releases.",
                "Replace Mammoth.",
            ),
            dependencies=(
                "aletheus.conclave",
                "aletheus.mammoth",
                "aletheus.ledger",
            ),
            consumes=(
                "quarantine_requests",
                "forensic_evidence",
            ),
            produces=(
                "quarantine_records",
                "forensic_snapshots",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.watch_tower",
                "aletheus.sentinel",
            ),
            certified_by=("aletheus.council",),
            repository_locations=(
                "archive/quarantine",
                "storage/quarantine",
            ),
            ontology_tags=(
                "quarantine",
                "evidence",
                "security",
            ),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.sentinel",
            canonical_name="Sentinel™",
            purpose=(
                "Provide continuous runtime monitoring, operational "
                "security, vitality assessment, and live defensive "
                "telemetry."
            ),
            authority="Runtime operational defense",
            jurisdiction="Active runtime",
            constitutional_layer=ConstitutionalLayer.RUNTIME,
            pillar=ConstitutionalPillar.INTELLIGENCE,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Monitor runtime security.",
                "Detect operational threats.",
                "Publish runtime telemetry.",
                "Enforce approved defensive controls.",
                "Protect containment boundaries.",
            ),
            non_responsibilities=(
                "Replace Watch Tower.",
                "Replace Guardian.",
                "Govern constitutional policy.",
                "Own quarantine evidence.",
            ),
            dependencies=(
                "aletheus.crk",
                "aletheus.guardian",
                "aletheus.conclave",
            ),
            consumes=(
                "runtime_telemetry",
                "security_events",
                "approved_defensive_actions",
                "containment_state",
            ),
            produces=(
                "runtime_security_signals",
                "threat_alerts",
                "operational_vitality",
                "defensive_enforcement_events",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.homeostasis",
                "aletheus.watch_tower",
            ),
            certified_by=("aletheus.council",),
            repository_locations=(
                "aletheus/runtime/sentinel",
                "reports/sentinel",
            ),
            ontology_tags=(
                "runtime",
                "security",
                "monitoring",
                "telemetry",
            ),
            genesis="12",
        ),
    )
