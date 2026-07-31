from aletheus.tooling.kinekt.orchestration.planner import build_units


def test_missing_candidates_causes_abstention() -> None:
    roadmap = {
        "work_packages": [
            {
                "package_id": "wp-empty",
                "title": "Empty",
                "phase": 1,
            }
        ]
    }

    units, abstentions = build_units(roadmap)

    assert units == []
    assert abstentions
