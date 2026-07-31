from __future__ import annotations

from aletheus.constitutional_events import (
    ConstitutionalEventFabric,
    LedgerEventSubscriber,
    SecurityEventType,
)
from aletheus.constitutional_ledger import ConstitutionalLedger
from aletheus.institutional_civilization import (
    SecurityCivilizationLifecycle,
)


class FakeGuardian:
    def classify(self, payload):
        return {
            "classification": "confirmed_integrity_threat",
            "severity": payload["severity"],
            "strategy": "contain",
        }


class FakeConclave:
    def contain(self, payload):
        return {
            "contained": True,
            "boundary": "SECURE-ZONE-001",
            "entity_id": payload["entity_id"],
        }


class FakeContainmentVault:
    def preserve(self, payload):
        return {
            "preserved": True,
            "vault_record_id": "VAULT-001",
            "chain_of_custody": True,
        }


class FakeSentinel:
    def stabilize(self, payload):
        return {
            "stabilized": True,
            "monitoring": "active",
        }


def build_lifecycle():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()

    fabric.subscribe_all(
        LedgerEventSubscriber(ledger),
        subscriber_name="constitutional_ledger",
    )

    lifecycle = SecurityCivilizationLifecycle(
        fabric=fabric,
        guardian=FakeGuardian(),
        conclave=FakeConclave(),
        containment_vault=FakeContainmentVault(),
        sentinel=FakeSentinel(),
    )
    lifecycle.install()

    return lifecycle, fabric, ledger


def test_security_lifecycle_registers_canonical_events():
    _, fabric, _ = build_lifecycle()

    assert fabric.registry.get(SecurityEventType.THREAT_CLASSIFIED) is not None
    assert fabric.registry.get(SecurityEventType.ENTITY_QUARANTINED) is not None
    assert fabric.registry.get(SecurityEventType.EVIDENCE_PRESERVED) is not None


def test_integrity_finding_runs_complete_defense_chain():
    lifecycle, fabric, _ = build_lifecycle()

    case = lifecycle.raise_integrity_finding(
        entity_id="plugin.untrusted",
        severity="critical",
        finding={
            "finding": "Unsigned executable behavior detected.",
        },
    )

    assert case.status == "stabilized"

    history = lifecycle.history(case.case_id)

    assert [event.event_type.value for event in history] == [
        "IntegrityFindingCreated",
        "ThreatClassified",
        "EntityQuarantined",
        "EvidencePreserved",
        "SecurityIncidentStabilized",
    ]

    assert fabric.health()["failed_deliveries"] == 0


def test_security_history_is_recorded_in_ledger():
    lifecycle, _, ledger = build_lifecycle()

    case = lifecycle.raise_integrity_finding(
        entity_id="runtime.component",
        severity="high",
        finding={
            "finding": "Unexpected dependency mutation.",
        },
    )

    replay = ledger.replay_events(correlation_id=case.correlation_id)

    assert len(replay) == 5
    assert replay[0].source_identity == ("aletheus.watch_tower")
    assert replay[-1].source_identity == ("aletheus.sentinel")


def test_transtemporal_lineage_follows_defense_chain():
    lifecycle, _, ledger = build_lifecycle()

    case = lifecycle.raise_integrity_finding(
        entity_id="repository.module",
        severity="critical",
        finding={
            "finding": "Constitutional boundary violation.",
        },
    )

    terminal_event_id = case.event_ids[-1]
    lineage = ledger.temporal_lineage(terminal_event_id)

    assert [event.event_type for event in lineage] == [
        "IntegrityFindingCreated",
        "ThreatClassified",
        "EntityQuarantined",
        "EvidencePreserved",
        "SecurityIncidentStabilized",
    ]


def test_default_adapters_remain_explicit_and_operational():
    ledger = ConstitutionalLedger()
    fabric = ConstitutionalEventFabric()
    fabric.subscribe_all(LedgerEventSubscriber(ledger))

    lifecycle = SecurityCivilizationLifecycle(fabric=fabric)

    case = lifecycle.raise_integrity_finding(
        entity_id="unknown.entity",
        severity="medium",
        finding={
            "finding": "Unclassified anomaly.",
        },
    )

    assert case.status == "stabilized"
    assert lifecycle.health()["stabilized"] == 1


def test_installation_is_idempotent():
    lifecycle, fabric, _ = build_lifecycle()

    subscriptions_before = fabric.health()["subscriptions"]

    lifecycle.install()

    subscriptions_after = fabric.health()["subscriptions"]

    assert subscriptions_after == subscriptions_before
