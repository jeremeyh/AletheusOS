import json

from aletheus.tooling.mission_control.engine import MissionControlEngine


def test_mission_control_creates_missions(tmp_path) -> None:
    observatory = tmp_path / "observatory.json"
    orchestration = tmp_path / "orchestration.json"
    observatory.write_text(json.dumps({"readiness": "not_ready"}))
    orchestration.write_text(
        json.dumps(
            {
                "units": [
                    {
                        "unit_id": "eu-one",
                        "title": "One",
                        "preconditions": ["approval"],
                    }
                ]
            }
        )
    )

    report = MissionControlEngine(
        observatory,
        orchestration,
        tmp_path / "out",
    ).plan()

    assert len(report.missions) == 1
    assert report.blocked_reasons
