from __future__ import annotations

from aletheus.platform_surface import (
    AletheusPlatform,
    build_aletheus_platform,
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
            "boundary": "PLATFORM-SURFACE-ZONE",
        }


class FakeContainmentVault:
    def preserve(self, payload):
        return {
            "preserved": True,
            "chain_of_custody": True,
            "vault_record_id": "PLATFORM-VAULT-001",
        }


class FakeSentinel:
    def stabilize(self, payload):
        return {
            "stabilized": True,
            "monitoring": "active",
        }


def build_platform():
    return build_aletheus_platform(
        guardian=FakeGuardian(),
        conclave=FakeConclave(),
        containment_vault=(
            FakeContainmentVault()
        ),
        sentinel=FakeSentinel(),
    )


def test_builds_stable_platform_facade():
    platform = build_platform()

    assert isinstance(
        platform,
        AletheusPlatform,
    )
    assert platform.runtime is not None
    assert platform.security is not None
    assert platform.cases is not None
    assert platform.missions is not None
    assert platform.ledger is not None


def test_security_surface_executes_complete_response():
    platform = build_platform()

    response = (
        platform
        .security
        .respond_to_integrity_finding(
            entity_id="platform.plugin",
            severity="critical",
            finding={
                "finding": (
                    "Platform Surface security proof."
                ),
            },
        )
    )

    assert response.case_status == "closed"
    assert response.mission_status == "completed"
    assert response.security_status == "stabilized"


def test_case_and_mission_surfaces_resolve_response():
    platform = build_platform()

    response = (
        platform
        .security
        .respond_to_integrity_finding(
            entity_id="platform.runtime",
            severity="high",
            finding={
                "finding": "Runtime mutation.",
            },
        )
    )

    case = platform.cases.require(
        response.case_id
    )
    mission = platform.missions.require(
        response.mission_id
    )

    assert case.case_id == response.case_id
    assert mission.mission_id == (
        response.mission_id
    )
    assert mission.case_id == case.case_id


def test_platform_runtime_snapshot_is_read_only_projection():
    platform = build_platform()

    platform.security.respond_to_integrity_finding(
        entity_id="platform.snapshot",
        severity="medium",
        finding={
            "finding": "Snapshot proof.",
        },
    )

    snapshot = platform.snapshot()

    assert snapshot.status == "healthy"
    assert snapshot.cases == 1
    assert snapshot.missions == 1
    assert snapshot.time_missions == 1
    assert snapshot.time_phases == 5
    assert snapshot.mission_executions == 1
    assert snapshot.phase_executions == 5
    assert snapshot.domain_events_published == 4
    assert snapshot.failures == 0


def test_ledger_surface_exposes_correlated_history():
    platform = build_platform()

    response = (
        platform
        .security
        .respond_to_integrity_finding(
            entity_id="platform.history",
            severity="critical",
            finding={
                "finding": (
                    "Ledger Surface proof."
                ),
            },
        )
    )

    history = platform.ledger.history(
        correlation_id=(
            response.correlation_id
        )
    )

    event_types = {
        event.event_type
        for event in history
    }

    assert "CaseDetected" in event_types
    assert "MissionCreated" in event_types
    assert "IntegrityFindingCreated" in event_types
    assert "ThreatClassified" in event_types
    assert "EntityQuarantined" in event_types
    assert "MissionTemporalSequenceCompleted" in (
        event_types
    )
    assert "CaseClosed" in event_types


def test_platform_health_composes_internal_health():
    platform = build_platform()

    health = platform.health()

    assert health.healthy
    assert health.status == "healthy"
    assert "orchestrator" in health.components
    assert "case_engine" in health.components
    assert "mission_engine" in health.components
    assert "time" in health.components
    assert "mission_runtime" in health.components
