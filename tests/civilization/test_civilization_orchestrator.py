from __future__ import annotations

from aletheus.civilization import (
    build_civilization_orchestrator,
)


class FakeGuardian:
    def classify(self, payload):
        return {
            "classification": "confirmed_threat",
            "severity": payload["severity"],
            "strategy": "contain",
        }


class FakeConclave:
    def contain(self, payload):
        return {
            "contained": True,
            "boundary": "SECURE-ZONE-ORCHESTRATED",
            "entity_id": payload["entity_id"],
        }


class FakeContainmentVault:
    def preserve(self, payload):
        return {
            "preserved": True,
            "vault_record_id": "VAULT-ORCHESTRATED-001",
            "chain_of_custody": True,
        }


class FakeSentinel:
    def stabilize(self, payload):
        return {
            "stabilized": True,
            "monitoring": "active",
        }


def build_orchestrator():
    return build_civilization_orchestrator(
        guardian=FakeGuardian(),
        conclave=FakeConclave(),
        containment_vault=FakeContainmentVault(),
        sentinel=FakeSentinel(),
    )


def test_orchestrates_complete_security_response():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="plugin.untrusted",
        severity="critical",
        finding={
            "finding": "Unsigned executable behavior detected.",
        },
    )

    assert response.case_status == "closed"
    assert response.mission_status == "completed"
    assert response.security_status == "stabilized"
    assert response.evidence_count == 5
    assert response.event_count > 0


def test_case_and_mission_share_correlation_history():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="runtime.component",
        severity="high",
        finding={
            "finding": "Unexpected runtime mutation.",
        },
    )

    history = orchestrator.history(
        response.correlation_id
    )

    event_types = [
        event.event_type
        for event in history
    ]

    assert "CaseDetected" in event_types
    assert "MissionCreated" in event_types
    assert "IntegrityFindingCreated" in event_types
    assert "ThreatClassified" in event_types
    assert "EntityQuarantined" in event_types
    assert "EvidencePreserved" in event_types
    assert "SecurityIncidentStabilized" in event_types
    assert "MissionCompleted" in event_types
    assert "CaseClosed" in event_types


def test_orchestrator_automatically_attaches_mission_to_case():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="repository.module",
        severity="critical",
        finding={
            "finding": "Constitutional boundary violation.",
        },
    )

    case = orchestrator.case_engine.registry.require(
        response.case_id
    )
    mission = orchestrator.mission_engine.registry.require(
        response.mission_id
    )

    assert mission.case_id == case.case_id
    assert mission.mission_id in case.mission_ids
    assert mission.correlation_id == case.correlation_id


def test_orchestrator_automatically_projects_security_evidence():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="dependency.graph",
        severity="high",
        finding={
            "finding": "Unexpected circular dependency.",
        },
    )

    case = orchestrator.case_engine.registry.require(
        response.case_id
    )
    mission = orchestrator.mission_engine.registry.require(
        response.mission_id
    )

    case_evidence = {
        item["evidence_type"]
        for item in case.evidence
    }
    mission_evidence = {
        item["evidence_type"]
        for item in mission.evidence
    }

    expected = {
        "integrity_finding",
        "threat_classification",
        "containment_result",
        "forensic_preservation",
        "stabilization_result",
    }

    assert case_evidence == expected
    assert mission_evidence == expected


def test_transtemporal_history_contains_entire_response():
    orchestrator = build_orchestrator()

    response = orchestrator.respond_to_integrity_finding(
        entity_id="service.runtime",
        severity="medium",
        finding={
            "finding": "Operational anomaly.",
        },
    )

    history = orchestrator.history(
        response.correlation_id
    )

    assert history[0].event_type == "CaseDetected"
    assert history[-1].event_type == "CaseClosed"

    source_identities = {
        event.source_identity
        for event in history
    }

    assert "aletheus.case_engine" in source_identities
    assert "aletheus.mission_engine" in source_identities
    assert "aletheus.watch_tower" in source_identities
    assert "aletheus.guardian" in source_identities
    assert "aletheus.conclave" in source_identities
    assert "aletheus.containment_vault" in source_identities
    assert "aletheus.sentinel" in source_identities


def test_default_security_adapters_support_full_orchestration():
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
    assert orchestrator.health()["failures"] == 0
