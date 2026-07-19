"""Canonical AletheusOS Civilization catalog."""

from __future__ import annotations

from .civilization_models import (
    CivilizationCriticality,
    CivilizationRecord,
    CivilizationStatus,
)


def canonical_civilizations() -> tuple[CivilizationRecord, ...]:
    return (
        CivilizationRecord(
            civilization_id="aletheus.civilization.governance",
            canonical_name="Governance Civilization™",
            purpose=(
                "Preserve constitutional authority, deliberation, "
                "oversight, policy, historical accountability, and "
                "governed institutional evolution."
            ),
            authority_domain="Constitutional governance",
            institution_ids=(
                "aletheus.council",
                "aletheus.watch_tower",
                "aletheus.ledger",
                "aletheus.constitutional_graph",
                "aletheus.constitutional_library",
            ),
            responsibilities=(
                "Govern consequential institutional decisions.",
                "Preserve constitutional accountability.",
                "Maintain policy and oversight boundaries.",
            ),
            non_responsibilities=(
                "Execute application-domain work directly.",
                "Replace bounded runtime institutions.",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            collaborates_with=(
                "aletheus.civilization.security",
                "aletheus.civilization.intelligence",
                "aletheus.civilization.runtime",
            ),
            status=CivilizationStatus.OPERATIONAL,
            criticality=CivilizationCriticality.CONSTITUTIONAL,
            ontology_tags=(
                "governance",
                "constitution",
                "oversight",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.security",
            canonical_name="Security Civilization™",
            purpose=(
                "Detect, classify, contain, preserve evidence of, "
                "and respond to threats against AletheusOS."
            ),
            authority_domain="Constitutional security and defense",
            institution_ids=(
                "aletheus.watch_tower",
                "aletheus.guardian",
                "aletheus.conclave",
                "aletheus.containment_vault",
                "aletheus.sentinel",
            ),
            responsibilities=(
                "Detect integrity and security threats.",
                "Coordinate defensive strategy.",
                "Contain suspicious or compromised entities.",
                "Preserve forensic evidence.",
                "Provide continuous runtime defense.",
            ),
            non_responsibilities=(
                "Make unrelated architectural recommendations.",
                "Replace Council governance.",
                "Destroy evidence without governed authorization.",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            collaborates_with=(
                "aletheus.civilization.governance",
                "aletheus.civilization.runtime",
                "aletheus.civilization.intelligence",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CONSTITUTIONAL,
            ontology_tags=(
                "security",
                "defense",
                "containment",
                "quarantine",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.intelligence",
            canonical_name="Intelligence Civilization™",
            purpose=(
                "Observe, analyze, understand, forecast, and explain "
                "the architecture and operating environment."
            ),
            authority_domain="Platform and domain intelligence",
            institution_ids=(
                "aletheus.spa",
                "aletheus.atlas",
                "aletheus.oracle",
                "aletheus.repository_dna",
                "aletheus.breadth",
                "aletheus.constellation",
            ),
            responsibilities=(
                "Produce architectural and predictive intelligence.",
                "Maintain structural and relational awareness.",
                "Expose inspectable findings and forecasts.",
            ),
            non_responsibilities=(
                "Make final constitutional decisions.",
                "Execute remediation without authorization.",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.watch_tower",
                "aletheus.homeostasis",
            ),
            collaborates_with=(
                "aletheus.civilization.governance",
                "aletheus.civilization.security",
                "aletheus.civilization.decision",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CRITICAL,
            ontology_tags=(
                "intelligence",
                "analysis",
                "forecasting",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.runtime",
            canonical_name="Runtime Civilization™",
            purpose=(
                "Compose, coordinate, schedule, execute, observe, and "
                "stabilize the operating institutions of AletheusOS."
            ),
            authority_domain="Constitutional runtime execution",
            institution_ids=(
                "aletheus.crk",
                "aletheus.event_fabric",
                "aletheus.mission_engine",
                "aletheus.time",
                "aletheus.hour_glass",
                "aletheus.homeostasis",
                "aletheus.service_registry",
                "aletheus.runtime_registry",
            ),
            responsibilities=(
                "Compose bounded platform services.",
                "Coordinate institutional execution.",
                "Maintain runtime readiness and equilibrium.",
                "Route constitutional events and missions.",
            ),
            non_responsibilities=(
                "Absorb domain-specific implementation logic.",
                "Replace governance or historical reasoning.",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.sentinel",
                "aletheus.watch_tower",
            ),
            collaborates_with=(
                "aletheus.civilization.governance",
                "aletheus.civilization.security",
                "aletheus.civilization.persistence",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CONSTITUTIONAL,
            ontology_tags=(
                "runtime",
                "execution",
                "composition",
                "scheduling",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.decision",
            canonical_name="Decision Civilization™",
            purpose=(
                "Transform evidence, knowledge, reasoning, risk, bias, "
                "and prediction into inspectable decision intelligence."
            ),
            authority_domain="Decision intelligence",
            institution_ids=(
                "aletheus.evidence_engine",
                "aletheus.knowledge_engine",
                "aletheus.reason_engine",
                "aletheus.memory_engine",
                "aletheus.risk_engine",
                "aletheus.predictive_engine",
                "aletheus.bias_engine",
            ),
            responsibilities=(
                "Produce bounded decision intelligence.",
                "Expose confidence, uncertainty, and evidence.",
                "Support THORᵡ decision grading.",
            ),
            non_responsibilities=(
                "Treat THORᵡ as an institution.",
                "Make Council decisions.",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            collaborates_with=(
                "aletheus.civilization.intelligence",
                "aletheus.civilization.governance",
                "aletheus.civilization.application",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CRITICAL,
            ontology_tags=(
                "decision",
                "evidence",
                "reasoning",
                "risk",
            ),
            metadata={
                "constitutional_instrument": "THORᵡ™",
            },
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.experience",
            canonical_name="Experience Civilization™",
            purpose=(
                "Compose and govern constitutional human and machine "
                "experiences across AletheusOS."
            ),
            authority_domain="Experience composition",
            institution_ids=(
                "aletheus.nimble",
                "aletheus.primitive_experience_library",
                "aletheus.experience_gateway",
            ),
            responsibilities=(
                "Compose constitutional experiences.",
                "Maintain experience consistency and accessibility.",
                "Expose platform intelligence through governed interfaces.",
            ),
            non_responsibilities=(
                "Own application-domain intelligence.",
                "Replace runtime or persistence institutions.",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            collaborates_with=(
                "aletheus.civilization.runtime",
                "aletheus.civilization.application",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CRITICAL,
            ontology_tags=(
                "experience",
                "interface",
                "composition",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.persistence",
            canonical_name="Persistence Civilization™",
            purpose=(
                "Provide governed storage, persistence, archival, "
                "indexing, recovery, replication, and data lifecycle."
            ),
            authority_domain="Universal persistence",
            institution_ids=(
                "aletheus.mammoth",
                "aletheus.ledger",
                "aletheus.memory_mesh",
                "aletheus.unified_cognitive_index",
                "aletheus.transtemporal",
            ),
            responsibilities=(
                "Preserve durable platform data.",
                "Maintain archival and recovery capabilities.",
                "Support empirical historical and temporal inquiry.",
            ),
            non_responsibilities=(
                "Decide what should be remembered.",
                "Own relative or absolute execution time.",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.homeostasis",
                "aletheus.sentinel",
            ),
            collaborates_with=(
                "aletheus.civilization.runtime",
                "aletheus.civilization.governance",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CONSTITUTIONAL,
            ontology_tags=(
                "storage",
                "history",
                "persistence",
                "recovery",
            ),
        ),
        CivilizationRecord(
            civilization_id="aletheus.civilization.application",
            canonical_name="Application Civilization™",
            purpose=(
                "Host governed applications that consume AletheusOS "
                "institutions, intelligence, runtime, and experience systems."
            ),
            authority_domain="Application realization",
            institution_ids=(
                "aletheus.card_hawk",
                "aletheus.enterprise",
                "aletheus.sentinel_application",
                "aletheus.forge",
                "aletheus.capital",
            ),
            responsibilities=(
                "Deliver domain-specific outcomes.",
                "Prove platform capabilities through real applications.",
                "Preserve constitutional boundaries from the platform.",
            ),
            non_responsibilities=(
                "Redefine platform constitutional authority.",
                "Absorb universal platform frameworks.",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.watch_tower",
                "aletheus.homeostasis",
            ),
            collaborates_with=(
                "aletheus.civilization.experience",
                "aletheus.civilization.decision",
                "aletheus.civilization.runtime",
            ),
            status=CivilizationStatus.ENGINEERING,
            criticality=CivilizationCriticality.CRITICAL,
            ontology_tags=(
                "applications",
                "products",
                "domains",
            ),
        ),
    )
