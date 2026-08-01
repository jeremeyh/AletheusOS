import asyncio
import json

from aletheus.tooling.end_to_end_mission.engine import MissionExecutionEngine


def test_mission_runs_from_evidence_to_certification(tmp_path) -> None:
    grid = tmp_path / "grid.json"
    bus = tmp_path / "bus.json"
    grid.write_text(
        json.dumps(
            {
                "steps": [
                    {"step_id": "1", "stage": "Evidence Validation"},
                    {"step_id": "2", "stage": "Platform Certification"},
                ]
            }
        )
    )
    bus.write_text(json.dumps({"channels": []}))
    report = asyncio.run(
        MissionExecutionEngine(grid, bus, tmp_path / "out").execute(
            "mission-1",
            {"asset": "example"},
        )
    )
    assert report["status"] == "completed"
    assert report["platform_certification"] == "READY"
    assert report["event_trace"] == [
        "evidence.created",
        "execution.completed",
        "platform.certified",
    ]
