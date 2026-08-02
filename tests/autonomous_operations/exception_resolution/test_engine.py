from aletheus.autonomous_operations.common import (
    MissionSnapshot,
    MissionStatus,
    OperationalEvent,
    Severity,
    TelemetrySample,
)
from aletheus.autonomous_operations.exception_resolution.engine import Engine


def test_exception_resolution_is_bounded_and_deterministic() -> None:
    mission = MissionSnapshot(
        mission_id="mission-1",
        objective="Operate constitutionally",
        status=MissionStatus.ACTIVATED,
        progress=0.5,
        confidence=0.9,
        risk=0.2,
        constitutional_score=1.0,
        deadline_epoch=600,
        last_updated_epoch=100,
        evidence_epoch=100,
    )
    event = OperationalEvent(
        event_id="event-1",
        mission_id=mission.mission_id,
        event_type="HEARTBEAT",
        severity=Severity.INFO,
        timestamp_epoch=110,
    )
    sample = TelemetrySample("error_rate", 0.1, 110)
    _ = (event, sample)
    result = Engine().resolve(mission, "RATE_LIMIT", 1)
    assert isinstance(result, dict)
    assert result["immutableDecisionContract"] is True
    assert result["humanAuthorityPreserved"] is True
    assert result["silentExternalExecution"] is False
    assert len(result["digest"]) == 64
