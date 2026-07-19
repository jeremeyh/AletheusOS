"""Canonical AletheusOS institution catalog."""

from __future__ import annotations

from .models import (
    ConstitutionalLayer,
    ConstitutionalPillar,
    InstitutionCriticality,
    InstitutionRecord,
    InstitutionStatus,
)


def canonical_institutions() -> tuple[InstitutionRecord, ...]:
    """Return the initial canonical institution catalog."""

    return (
        InstitutionRecord(
            institution_id="aletheus.crk",
            canonical_name="Constitutional Runtime Kernel™",
            purpose=(
                "Compose, initialize, coordinate, and expose the bounded "
                "runtime institutions of AletheusOS."
            ),
            authority="Constitutional runtime composition",
            jurisdiction="Platform runtime",
            constitutional_layer=ConstitutionalLayer.RUNTIME,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Compose bounded runtime capabilities.",
                "Coordinate platform startup and shutdown.",
                "Expose runtime services through stable contracts.",
            ),
            non_responsibilities=(
                "Absorb implementation logic from bounded services.",
                "Perform domain-specific application behavior.",
            ),
            consumes=(
                "aletheus.service_registry",
                "aletheus.event_bus",
                "aletheus.constitutional_graph",
            ),
            produces=(
                "runtime_context",
                "runtime_lifecycle_events",
            ),
            governed_by=("aletheus.council",),
            observed_by=(
                "aletheus.watch_tower",
                "aletheus.homeostasis",
            ),
            repository_locations=(
                "aletheus/runtime",
                "aletheus/platform_intelligence/constitutional_runtime_kernel",
            ),
            ontology_tags=("runtime", "kernel", "composition"),
            genesis="9",
        ),
        InstitutionRecord(
            institution_id="aletheus.repository_dna",
            canonical_name="Repository DNA™",
            purpose=(
                "Observe and preserve repository structure, lineage, "
                "genealogy, and implementation relationships."
            ),
            authority="Repository lineage",
            jurisdiction="Source repository",
            constitutional_layer=ConstitutionalLayer.INTELLIGENCE,
            pillar=ConstitutionalPillar.INTELLIGENCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CRITICAL,
            responsibilities=(
                "Inventory repository subsystems.",
                "Detect implementation collisions and lineage relationships.",
                "Publish repository observations for architectural analysis.",
            ),
            non_responsibilities=(
                "Judge architectural fitness.",
                "Enforce constitutional remediation.",
            ),
            consumes=("source_repository",),
            produces=(
                "repository_inventory",
                "repository_lineage",
                "collision_candidates",
            ),
            observed_by=("aletheus.watch_tower",),
            governed_by=("aletheus.council",),
            repository_locations=(
                "aletheus/repository_dna",
                "engineering/repository_dna",
            ),
            ontology_tags=("repository", "lineage", "observation"),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.ledger",
            canonical_name="Constitutional Ledger™",
            purpose=(
                "Preserve authoritative constitutional decisions, evidence, "
                "lineage, and institutional history."
            ),
            authority="Authoritative constitutional history",
            jurisdiction="Historical record",
            constitutional_layer=ConstitutionalLayer.MEMORY,
            pillar=ConstitutionalPillar.MEMORY,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Record certified constitutional history.",
                "Preserve evidence and decision lineage.",
                "Support replay and historical retrieval.",
            ),
            non_responsibilities=(
                "Decide what action should be taken.",
                "Replace Mammoth as the universal storage framework.",
            ),
            consumes=(
                "constitutional_decisions",
                "institutional_events",
                "certified_evidence",
            ),
            produces=(
                "ledger_entries",
                "decision_lineage",
                "historical_replay",
            ),
            observed_by=("aletheus.homeostasis",),
            governed_by=("aletheus.council",),
            repository_locations=("aletheus/constitutional_ledger",),
            ontology_tags=("memory", "history", "provenance"),
            genesis="19.4",
        ),
        InstitutionRecord(
            institution_id="aletheus.spa",
            canonical_name="Spectrum Platform Analyzer™",
            purpose="Analyze the structural health of AletheusOS.",
            authority="Architectural analysis",
            jurisdiction="Platform architecture",
            constitutional_layer=ConstitutionalLayer.INTELLIGENCE,
            pillar=ConstitutionalPillar.INTELLIGENCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CRITICAL,
            responsibilities=(
                "Analyze architectural fitness.",
                "Detect structural drift and dependency pressure.",
                "Produce inspectable architectural findings.",
            ),
            non_responsibilities=(
                "Modify source code.",
                "Make constitutional governance decisions.",
            ),
            consumes=(
                "aletheus.repository_dna",
                "aletheus.constitutional_graph",
                "aletheus.platform_registry",
            ),
            produces=(
                "architectural_findings",
                "platform_fitness_scores",
                "structural_recommendations",
            ),
            observed_by=("aletheus.watch_tower",),
            governed_by=("aletheus.council",),
            repository_locations=(
                "aletheus/spa",
                "aletheus/spectrum_platform_analyzer",
            ),
            ontology_tags=("architecture", "analysis", "fitness"),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.watch_tower",
            canonical_name="Watch Tower™",
            purpose=(
                "Protect institutional and architectural integrity through "
                "continuous constitutional oversight."
            ),
            authority="Constitutional oversight",
            jurisdiction="Platform integrity",
            constitutional_layer=ConstitutionalLayer.GOVERNANCE,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Assess constitutional significance of structured findings.",
                "Track integrity violations and remediation state.",
                "Escalate consequential findings for governance.",
            ),
            non_responsibilities=(
                "Perform raw source-code discovery.",
                "Make final Council decisions.",
            ),
            consumes=(
                "architectural_findings",
                "repository_integrity_signals",
                "constitutional_policy",
            ),
            produces=(
                "oversight_findings",
                "integrity_alerts",
                "governance_escalations",
            ),
            observed_by=("aletheus.homeostasis",),
            governed_by=("aletheus.council",),
            repository_locations=(
                "aletheus/watch_tower",
                "watch_tower",
            ),
            ontology_tags=("oversight", "integrity", "governance"),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.council",
            canonical_name="Council™",
            purpose=(
                "Deliberate on consequential constitutional matters and "
                "produce governed decisions."
            ),
            authority="Constitutional deliberation",
            jurisdiction="Platform governance",
            constitutional_layer=ConstitutionalLayer.GOVERNANCE,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Review consequential findings.",
                "Deliberate using constitutional evidence.",
                "Approve, reject, or condition governance proposals.",
            ),
            non_responsibilities=(
                "Execute remediation directly.",
                "Perform structural repository analysis.",
            ),
            consumes=(
                "governance_escalations",
                "constitutional_evidence",
                "risk_assessments",
            ),
            produces=(
                "constitutional_decisions",
                "approved_actions",
                "governance_conditions",
            ),
            observed_by=("aletheus.homeostasis",),
            repository_locations=(
                "aletheus/council",
                "aletheus/council_deliberation",
            ),
            ontology_tags=("governance", "deliberation", "decision"),
            genesis="9",
        ),
        InstitutionRecord(
            institution_id="aletheus.homeostasis",
            canonical_name="Homeostasis™",
            purpose=(
                "Measure and coordinate the equilibrium, resilience, and "
                "adaptive stability of the AletheusOS civilization."
            ),
            authority="Civilizational equilibrium",
            jurisdiction="Cross-platform health",
            constitutional_layer=ConstitutionalLayer.CROSS_CUTTING,
            pillar=ConstitutionalPillar.GOVERNANCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Synthesize institutional health signals.",
                "Detect constitutional imbalance.",
                "Coordinate bounded recovery recommendations.",
            ),
            non_responsibilities=(
                "Replace the institutions that produce health evidence.",
                "Unilaterally bypass constitutional governance.",
            ),
            consumes=(
                "platform_health_signals",
                "architectural_findings",
                "oversight_findings",
                "runtime_telemetry",
            ),
            produces=(
                "equilibrium_assessments",
                "stress_signals",
                "recovery_recommendations",
            ),
            governed_by=("aletheus.council",),
            repository_locations=("aletheus/homeostasis",),
            ontology_tags=("equilibrium", "health", "resilience"),
            genesis="12",
        ),
        InstitutionRecord(
            institution_id="aletheus.nimble",
            canonical_name="Nimble™",
            purpose=(
                "Compose and execute constitutional human experiences across "
                "AletheusOS applications."
            ),
            authority="Universal experience runtime",
            jurisdiction="Experience composition",
            constitutional_layer=ConstitutionalLayer.EXPERIENCE,
            pillar=ConstitutionalPillar.INTENT,
            status=InstitutionStatus.ENGINEERING,
            criticality=InstitutionCriticality.CRITICAL,
            responsibilities=(
                "Resolve and compose constitutional experiences.",
                "Execute the canonical experience lifecycle.",
                "Coordinate the Primitive Experience Library.",
            ),
            non_responsibilities=(
                "Own application-domain intelligence.",
                "Replace Mammoth persistence or CRK orchestration.",
            ),
            consumes=(
                "missions",
                "intents",
                "experience_definitions",
                "constitutional_objects",
            ),
            produces=(
                "composed_experiences",
                "experience_state",
                "experience_telemetry",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            repository_locations=("nimble",),
            ontology_tags=("experience", "composition", "runtime"),
            genesis="10",
        ),
        InstitutionRecord(
            institution_id="aletheus.mammoth",
            canonical_name="Mammoth™",
            purpose=(
                "Provide universal storage, persistence, archival, indexing, "
                "recovery, replication, and data lifecycle services."
            ),
            authority="Universal persistence",
            jurisdiction="Platform storage",
            constitutional_layer=ConstitutionalLayer.PERSISTENCE,
            pillar=ConstitutionalPillar.MEMORY,
            status=InstitutionStatus.PROPOSED,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Persist platform data according to constitutional policy.",
                "Provide archival, recovery, and indexing capabilities.",
                "Protect integrity across the data lifecycle.",
            ),
            non_responsibilities=(
                "Decide what the Memory Engine should remember.",
                "Interpret the meaning of stored information.",
            ),
            consumes=(
                "persistence_requests",
                "storage_policy",
                "lifecycle_policy",
            ),
            produces=(
                "durable_records",
                "indexes",
                "recovery_points",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            repository_locations=(
                "storage",
                "aletheus/persistence_v3",
            ),
            ontology_tags=("storage", "persistence", "lifecycle"),
            genesis="10",
        ),
        InstitutionRecord(
            institution_id="aletheus.thorx",
            canonical_name="THORᵡ™",
            purpose=(
                "Synthesize evidence, reasoning, risk, and predictive signals "
                "into inspectable strategic intelligence."
            ),
            authority="Strategic intelligence synthesis",
            jurisdiction="Decision intelligence",
            constitutional_layer=ConstitutionalLayer.INTELLIGENCE,
            pillar=ConstitutionalPillar.INTELLIGENCE,
            status=InstitutionStatus.IMPLEMENTED,
            criticality=InstitutionCriticality.CRITICAL,
            responsibilities=(
                "Synthesize multi-engine intelligence.",
                "Produce inspectable graded assessments.",
                "Expose uncertainty and supporting evidence.",
            ),
            non_responsibilities=(
                "Make constitutional governance decisions.",
                "Execute missions directly.",
            ),
            consumes=(
                "evidence",
                "reasoning",
                "risk_signals",
                "predictive_signals",
            ),
            produces=(
                "thorx_assessments",
                "strategic_recommendations",
                "confidence_grades",
            ),
            governed_by=("aletheus.council",),
            observed_by=("aletheus.homeostasis",),
            repository_locations=(
                "aletheus/thorx_runtime",
                "thorx",
                "card_hawk/thorx",
            ),
            ontology_tags=("intelligence", "synthesis", "assessment"),
            genesis="6",
        ),
        InstitutionRecord(
            institution_id="aletheus.breadth",
            canonical_name="Breadth™",
            purpose=(
                "Maintain platform-wide synthetic relationship awareness "
                "without replacing governance, truth, or execution."
            ),
            authority="Cross-system relationship awareness",
            jurisdiction="Civilizational awareness",
            constitutional_layer=ConstitutionalLayer.CROSS_CUTTING,
            pillar=ConstitutionalPillar.INTELLIGENCE,
            status=InstitutionStatus.CONSTITUTIONAL,
            criticality=InstitutionCriticality.CONSTITUTIONAL,
            responsibilities=(
                "Synthesize awareness across bounded institutions.",
                "Expose cross-system relationships and context.",
            ),
            non_responsibilities=(
                "Act as literal consciousness.",
                "Replace governance or execution authority.",
            ),
            consumes=(
                "institutional_context",
                "runtime_context",
                "mission_context",
            ),
            produces=(
                "relationship_awareness",
                "civilizational_context",
            ),
            governed_by=("aletheus.council",),
            repository_locations=("aletheus/breadth",),
            ontology_tags=("awareness", "relationships", "context"),
            genesis="8",
        ),
    )
