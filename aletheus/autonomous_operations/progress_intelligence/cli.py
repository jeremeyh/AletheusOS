from __future__ import annotations

from json import dumps

from ..common import (
    MissionSnapshot,
    MissionStatus,
    OperationalEvent,
    Severity,
    TelemetrySample,
)
from .engine import Engine


def main() -> None:
    mission = MissionSnapshot(
        mission_id="mission-demo",
        objective="Maintain a healthy constitutional mission",
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
        event_id="event-demo",
        mission_id=mission.mission_id,
        event_type="HEARTBEAT",
        severity=Severity.INFO,
        timestamp_epoch=110,
    )
    sample = TelemetrySample("error_rate", 0.1, 110)
    _ = (event, sample)
    result = Engine().measure(mission, 5.0, 10.0)
    print(dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
