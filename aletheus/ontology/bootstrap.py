from __future__ import annotations

from .models import (
    OntologyEntity,
    OntologyEntityType,
    OntologyRelationship,
    OntologyStatus,
    RelationshipType,
)
from .registry import OntologyRegistry, ontology_registry


CANONICAL_AUTHORITIES = [
    (
        "AUTH-ATLAS",
        "Atlas",
        "Atlas knows architecture.",
        "Platform Intelligence",
        "Architecture authority for topology, dependencies, structure, and Constellation.",
    ),
    (
        "AUTH-WATCH-TOWER",
        "Watch Tower",
        "Watch Tower knows repository integrity.",
        "Guardian",
        "Repository and architectural integrity authority.",
    ),
    (
        "AUTH-GUARDIAN",
        "Guardian",
        "Guardian knows coordinated defense.",
        "Security / Defense",
        "Coordinated defense authority across trust, threat, and response domains.",
    ),
    (
        "AUTH-CONCLAVE",
        "Conclave",
        "Conclave knows containment.",
        "Security / Defense",
        "Containment, isolation, and trust-boundary authority.",
    ),
    (
        "AUTH-SENTINEL",
        "Sentinel",
        "Sentinel knows operational health.",
        "Health / Stability",
        "Operational health, vitality, heartbeat, and resilience authority.",
    ),
    (
        "AUTH-COUNCIL",
        "Council",
        "Council knows governance.",
        "Constitutional",
        "Composite governance authority for constitutional decisions.",
    ),
    (
        "AUTH-ORACLE",
        "Oracle",
        "Oracle forecasts risk.",
        "Platform Intelligence",
        "Predictive authority for risk, trend, and future-state forecasting.",
    ),
    (
        "AUTH-GENESIS",
        "Genesis",
        "Genesis generates conformant scaffolding.",
        "Creation / Evolution",
        "Conformant architecture and project scaffolding authority.",
    ),
    (
        "AUTH-REPOSITORY-DNA",
        "Repository DNA",
        "Repository DNA knows history.",
        "Repository",
        "Architectural genealogy and implementation-history authority.",
    ),
    (
        "AUTH-CONSTELLATION",
        "Constellation",
        "Constellation knows visual topology.",
        "Platform Intelligence",
        "Visual topology authority powered by Atlas.",
    ),
    (
        "AUTH-CTF",
        "Cognitive Transit Fabric",
        "CTF knows transit.",
        "Transit",
        "Cognitive transit authority for routing intent, context, execution, and results.",
    ),
    (
        "AUTH-MEMORY-MESH",
        "Memory Mesh",
        "Memory Mesh knows continuity.",
        "Memory / Awareness",
        "Continuity authority for memory synchronization and persistence relationships.",
    ),
    (
        "AUTH-UCI",
        "Unified Cognitive Index",
        "Unified Cognitive Index knows discoverability.",
        "Memory / Awareness",
        "Discoverability authority for semantic lookup and cognitive indexing.",
    ),
    (
        "AUTH-HOMEOSTASIS",
        "Homeostasis",
        "Homeostasis knows equilibrium.",
        "Health / Stability",
        "Equilibrium and adaptive stability authority.",
    ),
    (
        "AUTH-AUTONOMIC",
        "Autonomic",
        "Autonomic knows self-regulation.",
        "Health / Stability",
        "Self-regulation authority for adaptive platform control.",
    ),
    (
        "AUTH-SPA",
        "Spectrum Platform Analyzer",
        "SPA knows architectural fitness.",
        "Observability",
        "Architectural fitness and analyzer authority; evaluates but does not govern or modify.",
    ),
    (
        "AUTH-RUNTIME",
        "Runtime",
        "Runtime knows execution.",
        "Execution",
        "Execution authority; coordinates and executes without absorbing unrelated domains.",
    ),
    (
        "AUTH-RUNTIME-REGISTRY-V2",
        "Runtime Registry v2",
        "Runtime Registry v2 knows registered capability.",
        "Execution",
        "Canonical runtime capability discovery and registration authority.",
    ),
    (
        "AUTH-BREADTH",
        "Breadth",
        "Breadth knows relationship awareness.",
        "Philosophy",
        "Platform-wide synthetic relationship awareness; not literal consciousness, governance, or execution.",
    ),
]


def seed_canonical_authorities(
    registry: OntologyRegistry = ontology_registry,
) -> None:
    """Register the current canonical authority sentences."""

    for entity_id, name, sentence, family, description in CANONICAL_AUTHORITIES:
        registry.register_entity(
            OntologyEntity(
                entity_id=entity_id,
                name=name,
                entity_type=OntologyEntityType.AUTHORITY,
                description=description,
                status=OntologyStatus.CANONICAL,
                family=family,
                authority=name,
                authority_sentence=sentence,
                tags=["authority", "canonical"],
            )
        )

    registry.register_entity(
        OntologyEntity(
            entity_id="PRINCIPLE-SYNTHETIC-HARMONY",
            name="Synthetic Harmony",
            entity_type=OntologyEntityType.PRINCIPLE,
            description=(
                "Emergent coherence property of the Super-Mesh; not an authority, "
                "fabric, layer, engine, service, registry, or circuit."
            ),
            status=OntologyStatus.CANONICAL,
            family="Philosophy",
            tags=["principle", "super-mesh", "emergent"],
        )
    )

    for entity in registry.all_entities():
        if entity.entity_id == "PRINCIPLE-SYNTHETIC-HARMONY":
            continue
        registry.register_relationship(
            OntologyRelationship(
                relationship_id=f"REL-{entity.entity_id}-INFLUENCES-HARMONY",
                source_entity_id="PRINCIPLE-SYNTHETIC-HARMONY",
                target_entity_id=entity.entity_id,
                relationship_type=RelationshipType.INFLUENCES,
                description="Synthetic Harmony influences every canonical authority.",
            )
        )
