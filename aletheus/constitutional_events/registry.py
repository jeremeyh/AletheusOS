"""Canonical registry for constitutional event types."""

from __future__ import annotations

from dataclasses import dataclass

from .models import ConstitutionalEventType


@dataclass(frozen=True, slots=True)
class EventTypeDefinition:
    event_type: ConstitutionalEventType
    description: str
    constitutional_domain: str
    requires_certification: bool = False

    def to_dict(self) -> dict:
        return {
            "event_type": self.event_type.value,
            "description": self.description,
            "constitutional_domain": self.constitutional_domain,
            "requires_certification": self.requires_certification,
        }


class DuplicateEventTypeError(ValueError):
    """Raised when an event type is registered more than once."""


class ConstitutionalEventRegistry:
    """Registry of event meanings, not event instances."""

    def __init__(self) -> None:
        self._definitions: dict[
            ConstitutionalEventType,
            EventTypeDefinition,
        ] = {}

    def register(
        self,
        definition: EventTypeDefinition,
        *,
        replace: bool = False,
    ) -> EventTypeDefinition:
        if (
            definition.event_type in self._definitions
            and not replace
        ):
            raise DuplicateEventTypeError(
                f"Event type {definition.event_type.value!r} "
                "is already registered."
            )

        self._definitions[definition.event_type] = definition
        return definition

    def get(
        self,
        event_type: ConstitutionalEventType,
    ) -> EventTypeDefinition | None:
        return self._definitions.get(event_type)

    def require(
        self,
        event_type: ConstitutionalEventType,
    ) -> EventTypeDefinition:
        definition = self.get(event_type)

        if definition is None:
            raise KeyError(
                f"Unregistered constitutional event type: "
                f"{event_type.value}"
            )

        return definition

    def list(self) -> tuple[EventTypeDefinition, ...]:
        return tuple(
            sorted(
                self._definitions.values(),
                key=lambda item: item.event_type.value,
            )
        )

    def statistics(self) -> dict:
        return {
            "event_types": len(self._definitions),
            "certification_required": sum(
                definition.requires_certification
                for definition in self._definitions.values()
            ),
            "domains": sorted({
                definition.constitutional_domain
                for definition in self._definitions.values()
            }),
        }


def canonical_event_definitions() -> tuple[EventTypeDefinition, ...]:
    """Return the initial constitutional event vocabulary."""

    descriptions = {
        ConstitutionalEventType.CIVILIZATION_BOOTSTRAP_STARTED: (
            "A constitutional civilization bootstrap has begun.",
            "runtime",
            False,
        ),
        ConstitutionalEventType.CIVILIZATION_BOOTSTRAP_COMPLETED: (
            "A civilization bootstrap completed with an inspectable result.",
            "runtime",
            False,
        ),
        ConstitutionalEventType.INSTITUTION_ESTABLISHED: (
            "A canonical institution was established.",
            "institution",
            True,
        ),
        ConstitutionalEventType.INSTITUTION_PROJECTED: (
            "An institution was projected into platform registries or graphs.",
            "institution",
            False,
        ),
        ConstitutionalEventType.INSTITUTION_HEALTH_CHANGED: (
            "The measured health of an institution changed.",
            "homeostasis",
            False,
        ),
        ConstitutionalEventType.WATCH_TOWER_ASSESSMENT_REQUESTED: (
            "A Watch Tower oversight assessment was requested.",
            "governance",
            False,
        ),
        ConstitutionalEventType.WATCH_TOWER_ASSESSMENT_COMPLETED: (
            "Watch Tower completed an oversight assessment.",
            "governance",
            False,
        ),
        ConstitutionalEventType.INTEGRITY_FINDING_CREATED: (
            "A constitutional integrity finding was created.",
            "governance",
            False,
        ),
        ConstitutionalEventType.PLATFORM_ASSESSMENT_REQUESTED: (
            "A Spectrum Platform Analyzer assessment was requested.",
            "intelligence",
            False,
        ),
        ConstitutionalEventType.PLATFORM_ASSESSMENT_COMPLETED: (
            "SPA completed an architectural assessment.",
            "intelligence",
            False,
        ),
        ConstitutionalEventType.COUNCIL_REVIEW_REQUESTED: (
            "A consequential matter was escalated to Council.",
            "governance",
            False,
        ),
        ConstitutionalEventType.COUNCIL_DECISION_RECORDED: (
            "Council produced a governed constitutional decision.",
            "governance",
            True,
        ),
        ConstitutionalEventType.HOMEOSTASIS_UPDATED: (
            "Homeostasis incorporated new institutional health signals.",
            "homeostasis",
            False,
        ),
        ConstitutionalEventType.SYNTHETIC_HARMONY_CHANGED: (
            "The measured coherence of the civilization changed.",
            "homeostasis",
            False,
        ),
        ConstitutionalEventType.LEDGER_ENTRY_CREATED: (
            "Ledger created an authoritative historical record.",
            "memory",
            True,
        ),
    }

    return tuple(
        EventTypeDefinition(
            event_type=event_type,
            description=description,
            constitutional_domain=domain,
            requires_certification=requires_certification,
        )
        for event_type, (
            description,
            domain,
            requires_certification,
        ) in descriptions.items()
    )


def build_canonical_event_registry() -> ConstitutionalEventRegistry:
    registry = ConstitutionalEventRegistry()

    for definition in canonical_event_definitions():
        registry.register(definition)

    return registry
