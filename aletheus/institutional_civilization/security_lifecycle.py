"""Event-driven lifecycle of the AletheusOS Security Civilization."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from aletheus.constitutional_events import (
    ConstitutionalEvent,
    ConstitutionalEventFabric,
)
from aletheus.constitutional_events.security import (
    SecurityEventType,
    register_security_event_types,
)


def _case_id() -> str:
    return f"SEC-{uuid4().hex[:12].upper()}"


def _mapping(value: Any) -> dict[str, Any]:
    if value is None:
        return {}

    if isinstance(value, dict):
        return value

    if hasattr(value, "to_dict"):
        result = value.to_dict()

        if isinstance(result, dict):
            return result

    return {"value": value}


@dataclass(slots=True)
class SecurityCase:
    case_id: str
    correlation_id: str
    entity_id: str
    severity: str
    status: str = "detected"
    event_ids: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "correlation_id": self.correlation_id,
            "entity_id": self.entity_id,
            "severity": self.severity,
            "status": self.status,
            "event_ids": list(self.event_ids),
            "evidence": list(self.evidence),
        }


class SecurityCivilizationLifecycle:
    """
    Event-driven security defense chain.

    Watch Tower discovers.
    Guardian classifies.
    Conclave contains.
    Containment Vault preserves.
    Sentinel stabilizes.
    Council governs consequential release or destruction.
    """

    VERSION = "0.1.0"

    def __init__(
        self,
        *,
        fabric: ConstitutionalEventFabric,
        guardian: Any | None = None,
        conclave: Any | None = None,
        containment_vault: Any | None = None,
        sentinel: Any | None = None,
    ) -> None:
        self.fabric = fabric
        self.guardian = guardian
        self.conclave = conclave
        self.containment_vault = containment_vault
        self.sentinel = sentinel

        self.cases: dict[str, SecurityCase] = {}
        self._installed = False
        self._handled = 0

        register_security_event_types(self.fabric.registry)

    def install(self) -> None:
        """Install canonical institutional subscriptions once."""

        if self._installed:
            return

        self.fabric.subscribe(
            SecurityEventType.INTEGRITY_FINDING_CREATED,
            self._handle_integrity_finding,
            subscriber_name="guardian",
        )
        self.fabric.subscribe(
            SecurityEventType.THREAT_CLASSIFIED,
            self._handle_threat_classified,
            subscriber_name="conclave",
        )
        self.fabric.subscribe(
            SecurityEventType.ENTITY_QUARANTINED,
            self._handle_entity_quarantined,
            subscriber_name="containment_vault",
        )
        self.fabric.subscribe(
            SecurityEventType.EVIDENCE_PRESERVED,
            self._handle_evidence_preserved,
            subscriber_name="sentinel",
        )

        self._installed = True

    def raise_integrity_finding(
        self,
        *,
        entity_id: str,
        severity: str,
        finding: dict[str, Any],
        correlation_id: str | None = None,
    ) -> SecurityCase:
        """Begin a governed security case from a Watch Tower finding."""

        self.install()

        case_id = _case_id()
        correlation = correlation_id or case_id

        case = SecurityCase(
            case_id=case_id,
            correlation_id=correlation,
            entity_id=entity_id,
            severity=severity,
            evidence=[dict(finding)],
        )
        self.cases[case_id] = case

        event = ConstitutionalEvent.create(
            SecurityEventType.INTEGRITY_FINDING_CREATED,
            "aletheus.watch_tower",
            correlation_id=correlation,
            payload={
                "case_id": case_id,
                "entity_id": entity_id,
                "severity": severity,
                "finding": dict(finding),
            },
            evidence=(dict(finding),),
            tags=(
                "security",
                "integrity",
                severity.casefold(),
            ),
        )

        case.event_ids.append(event.event_id)
        self.fabric.publish(event)
        return case

    def _handle_integrity_finding(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        self._handled += 1
        case = self._require_case(event)

        classification = self._classify(event)
        case.status = "classified"

        classified = ConstitutionalEvent.create(
            SecurityEventType.THREAT_CLASSIFIED,
            "aletheus.guardian",
            correlation_id=event.correlation_id,
            causation_id=event.event_id,
            payload={
                "case_id": case.case_id,
                "entity_id": case.entity_id,
                "severity": case.severity,
                "classification": classification,
            },
            evidence=event.evidence,
            tags=("security", "classification"),
        )

        case.event_ids.append(classified.event_id)
        self.fabric.publish(classified)
        return classification

    def _handle_threat_classified(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        self._handled += 1
        case = self._require_case(event)

        containment = self._contain(event)
        case.status = "quarantined"

        quarantined = ConstitutionalEvent.create(
            SecurityEventType.ENTITY_QUARANTINED,
            "aletheus.conclave",
            correlation_id=event.correlation_id,
            causation_id=event.event_id,
            payload={
                "case_id": case.case_id,
                "entity_id": case.entity_id,
                "severity": case.severity,
                "containment": containment,
            },
            evidence=event.evidence,
            tags=("security", "containment", "quarantine"),
        )

        case.event_ids.append(quarantined.event_id)
        self.fabric.publish(quarantined)
        return containment

    def _handle_entity_quarantined(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        self._handled += 1
        case = self._require_case(event)

        preservation = self._preserve(event)
        case.status = "evidence_preserved"
        case.evidence.append(preservation)

        preserved = ConstitutionalEvent.create(
            SecurityEventType.EVIDENCE_PRESERVED,
            "aletheus.containment_vault",
            correlation_id=event.correlation_id,
            causation_id=event.event_id,
            payload={
                "case_id": case.case_id,
                "entity_id": case.entity_id,
                "preservation": preservation,
            },
            evidence=(
                *event.evidence,
                preservation,
            ),
            tags=(
                "security",
                "forensics",
                "chain-of-custody",
            ),
        )

        case.event_ids.append(preserved.event_id)
        self.fabric.publish(preserved)
        return preservation

    def _handle_evidence_preserved(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        self._handled += 1
        case = self._require_case(event)

        stabilization = self._stabilize(event)
        case.status = "stabilized"

        stabilized = ConstitutionalEvent.create(
            SecurityEventType.SECURITY_INCIDENT_STABILIZED,
            "aletheus.sentinel",
            correlation_id=event.correlation_id,
            causation_id=event.event_id,
            payload={
                "case_id": case.case_id,
                "entity_id": case.entity_id,
                "stabilization": stabilization,
            },
            evidence=event.evidence,
            tags=("security", "runtime", "stabilized"),
        )

        case.event_ids.append(stabilized.event_id)
        self.fabric.publish(stabilized)
        return stabilization

    def _classify(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        if self.guardian is None:
            return {
                "classification": "unverified_threat",
                "severity": event.payload["severity"],
                "strategy": "contain",
                "adapter": "constitutional_default",
            }

        if hasattr(self.guardian, "classify"):
            return _mapping(self.guardian.classify(event.payload))

        if hasattr(self.guardian, "evaluate"):
            return _mapping(self.guardian.evaluate(event.payload))

        raise TypeError("Guardian exposes no classify or evaluate method.")

    def _contain(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        if self.conclave is None:
            return {
                "contained": True,
                "boundary": "default_secure_boundary",
                "adapter": "constitutional_default",
            }

        if hasattr(self.conclave, "contain"):
            return _mapping(self.conclave.contain(event.payload))

        if hasattr(self.conclave, "isolate"):
            return _mapping(self.conclave.isolate(event.payload))

        raise TypeError("Conclave exposes no contain or isolate method.")

    def _preserve(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        if self.containment_vault is None:
            return {
                "preserved": True,
                "vault": "containment_vault",
                "chain_of_custody": True,
                "adapter": "constitutional_default",
            }

        if hasattr(self.containment_vault, "preserve"):
            return _mapping(self.containment_vault.preserve(event.payload))

        if hasattr(self.containment_vault, "store"):
            return _mapping(self.containment_vault.store(event.payload))

        raise TypeError("Containment Vault exposes no preserve or store method.")

    def _stabilize(
        self,
        event: ConstitutionalEvent,
    ) -> dict[str, Any]:
        if self.sentinel is None:
            return {
                "stabilized": True,
                "monitoring": "active",
                "adapter": "constitutional_default",
            }

        if hasattr(self.sentinel, "stabilize"):
            return _mapping(self.sentinel.stabilize(event.payload))

        if hasattr(self.sentinel, "protect"):
            return _mapping(self.sentinel.protect(event.payload))

        raise TypeError("Sentinel exposes no stabilize or protect method.")

    def _require_case(
        self,
        event: ConstitutionalEvent,
    ) -> SecurityCase:
        case_id = event.payload.get("case_id")
        case = self.cases.get(case_id)

        if case is None:
            raise KeyError(f"Unknown security case: {case_id!r}")

        return case

    def get_case(
        self,
        case_id: str,
    ) -> SecurityCase | None:
        return self.cases.get(case_id)

    def history(
        self,
        case_id: str,
    ) -> tuple[ConstitutionalEvent, ...]:
        case = self.cases.get(case_id)

        if case is None:
            return ()

        return self.fabric.events(correlation_id=case.correlation_id)

    def health(self) -> dict[str, Any]:
        return {
            "name": "Security Civilization Lifecycle™",
            "version": self.VERSION,
            "status": "online",
            "installed": self._installed,
            "cases": len(self.cases),
            "handled_events": self._handled,
            "stabilized": sum(
                case.status == "stabilized" for case in self.cases.values()
            ),
        }
