"""Canonical event vocabulary of the AletheusOS Security Civilization."""

from __future__ import annotations

from enum import StrEnum

from .registry import (
    ConstitutionalEventRegistry,
    EventTypeDefinition,
)


class SecurityEventType(StrEnum):
    """
    Typed events used by the Security Civilization.

    INTEGRITY_FINDING_CREATED already belongs to the original constitutional
    event vocabulary. It is referenced here by its canonical string value,
    but it is not registered a second time.
    """

    INTEGRITY_FINDING_CREATED = "IntegrityFindingCreated"
    THREAT_CLASSIFIED = "ThreatClassified"

    CONTAINMENT_REQUESTED = "ContainmentRequested"
    ENTITY_QUARANTINED = "EntityQuarantined"

    EVIDENCE_PRESERVED = "EvidencePreserved"
    CHAIN_OF_CUSTODY_RECORDED = "ChainOfCustodyRecorded"

    SECURITY_INCIDENT_STABILIZED = "SecurityIncidentStabilized"

    RELEASE_REVIEW_REQUESTED = "ReleaseReviewRequested"
    RELEASE_AUTHORIZED = "ReleaseAuthorized"
    DESTRUCTION_AUTHORIZED = "DestructionAuthorized"

    ENTITY_RELEASED = "EntityReleased"
    ENTITY_DESTROYED = "EntityDestroyed"

    SECURITY_GOVERNANCE_ESCALATED = "SecurityGovernanceEscalated"


def canonical_security_event_definitions() -> tuple[EventTypeDefinition, ...]:
    """
    Return event definitions owned by the Security Civilization.

    IntegrityFindingCreated is intentionally excluded because it is already
    defined by the foundational Constitutional Event Fabric.
    """

    return (
        EventTypeDefinition(
            event_type=SecurityEventType.THREAT_CLASSIFIED,
            description=(
                "Guardian classified the defensive significance of a security finding."
            ),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.CONTAINMENT_REQUESTED,
            description=("Guardian or Council requested governed containment."),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.ENTITY_QUARANTINED,
            description=(
                "Conclave isolated an entity within a governed containment boundary."
            ),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.EVIDENCE_PRESERVED,
            description=("Containment Vault preserved forensic evidence."),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=(SecurityEventType.CHAIN_OF_CUSTODY_RECORDED),
            description=(
                "Containment Vault established an inspectable chain-of-custody record."
            ),
            constitutional_domain="security",
            requires_certification=True,
        ),
        EventTypeDefinition(
            event_type=(SecurityEventType.SECURITY_INCIDENT_STABILIZED),
            description=(
                "Sentinel confirmed that the active security incident "
                "was operationally stabilized."
            ),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.RELEASE_REVIEW_REQUESTED,
            description=("Conclave requested governed review of a quarantined entity."),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.RELEASE_AUTHORIZED,
            description=("Council authorized release of a quarantined entity."),
            constitutional_domain="governance",
            requires_certification=True,
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.DESTRUCTION_AUTHORIZED,
            description=(
                "Council authorized governed destruction of a quarantined entity."
            ),
            constitutional_domain="governance",
            requires_certification=True,
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.ENTITY_RELEASED,
            description=("Conclave released an entity from containment."),
            constitutional_domain="security",
        ),
        EventTypeDefinition(
            event_type=SecurityEventType.ENTITY_DESTROYED,
            description=(
                "A quarantined entity was destroyed under certified authorization."
            ),
            constitutional_domain="security",
            requires_certification=True,
        ),
        EventTypeDefinition(
            event_type=(SecurityEventType.SECURITY_GOVERNANCE_ESCALATED),
            description=(
                "Guardian escalated a consequential security matter to Council."
            ),
            constitutional_domain="governance",
        ),
    )


def register_security_event_types(
    registry: ConstitutionalEventRegistry,
) -> ConstitutionalEventRegistry:
    """
    Register Security Civilization-owned event definitions.

    Existing definitions with the same canonical value are accepted when
    semantically identical. Conflicting definitions remain prohibited.
    """

    for definition in canonical_security_event_definitions():
        existing = registry.get(definition.event_type)

        if existing is None:
            registry.register(definition)
            continue

        if (
            existing.event_type.value != definition.event_type.value
            or existing.constitutional_domain != definition.constitutional_domain
            or existing.requires_certification != definition.requires_certification
        ):
            raise ValueError(
                f"Conflicting event definition for {definition.event_type.value!r}."
            )

    return registry
