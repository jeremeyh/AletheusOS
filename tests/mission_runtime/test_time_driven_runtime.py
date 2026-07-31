from __future__ import annotations

from aletheus.civilization import (
    build_civilization_orchestrator,
)


class FakeWatchTower:
    def verify(self):
        return {
            "verified": True,
            "findings": 1,
        }


class FakeGuardian:
    def classify(self, payload):
        return {
            "classification": "confirmed_threat",
            "severity": "critical",
            "strategy": "contain",
        }


class FakeConclave:
    def contain(self, payload):
        return {
            "contained": True,
            "boundary": "SECURE-ZONE-TIME",
        }


class FakeContainmentVault:
    def preserve(self, payload):
        return {
            "preserved": True,
            "chain_of_custody": True,
            "vault_record_id": "VAULT-TIME-001",
        }


class FakeSentinel:
    def stabilize(self, payload):
        return {
            "stabilized": True,
            "monitoring": "active",
        }


def build_orchestrator():
    return build_civilization_orchestrator(
        watch_tower=FakeWatchTower(),
        guardian=FakeGuardian(),
        conclave=FakeConclave(),
        containment_vault=FakeContainmentVault(),
        sentinel=FakeSentinel(),
    )


def test_time_drives_complete_security_sequence():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="plugin.untrusted",
        severity="critical",
        finding={
            "finding": "Unsigned executable behavior.",
        },
    )

    assert response.case_status == "closed"
    assert response.mission_status == "completed"
    assert response.security_status == "stabilized"
    assert response.metadata["phase_order"] == [
        "detect",
        "classify",
        "contain",
        "preserve",
        "stabilize",
    ]


def test_time_events_are_preserved_in_ledger():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="runtime.module",
        severity="high",
        finding={
            "finding": "Unexpected mutation.",
        },
    )

    event_types = [
        event.event_type for event in orchestrator.history(response.correlation_id)
    ]

    assert "MissionPhaseGraphAttached" in event_types
    assert "MissionPhaseEligible" in event_types
    assert "MissionPhaseStarted" in event_types
    assert "MissionPhaseEvidenceAttached" in event_types
    assert "MissionPhaseCompleted" in event_types
    assert "MissionTemporalSequenceCompleted" in event_types


def test_phase_evidence_reaches_case_and_mission():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="repository.module",
        severity="high",
        finding={
            "finding": "Boundary violation.",
        },
    )

    case = orchestrator.case_engine.registry.require(response.case_id)
    mission = orchestrator.mission_engine.registry.require(response.mission_id)

    expected = {
        "integrity_finding",
        "threat_classification",
        "containment_result",
        "forensic_preservation",
        "stabilization_result",
    }

    assert {item["evidence_type"] for item in case.evidence} == expected

    assert {item["evidence_type"] for item in mission.evidence} == expected


def test_default_executors_support_time_runtime():
    orchestrator = build_civilization_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="unknown.entity",
        severity="medium",
        finding={
            "finding": "Unclassified anomaly.",
        },
    )

    assert response.case_status == "closed"
    assert response.mission_status == "completed"
    assert orchestrator.time.sequence_completed(response.mission_id)


def test_runtime_reports_execution_health():
    orchestrator = build_orchestrator()

    orchestrator.respond_to_integrity_finding(
        entity_id="service.runtime",
        severity="critical",
        finding={
            "finding": "Runtime integrity failure.",
        },
    )

    health = orchestrator.health()

    assert health["failures"] == 0
    assert health["mission_runtime"]["missions_executed"] == 1
    assert health["mission_runtime"]["phases_executed"] == 5


def test_runtime_publishes_security_domain_events():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="runtime.semantic-events",
        severity="critical",
        finding={
            "finding": ("Verify semantic Security Civilization events."),
        },
    )

    event_types = [
        event.event_type for event in orchestrator.history(response.correlation_id)
    ]

    assert "IntegrityFindingCreated" in event_types
    assert "ThreatClassified" in event_types
    assert "EntityQuarantined" in event_types
    assert "EvidencePreserved" in event_types
    assert "SecurityIncidentStabilized" in event_types

    assert orchestrator.health()["mission_runtime"]["domain_events_published"] == 4
