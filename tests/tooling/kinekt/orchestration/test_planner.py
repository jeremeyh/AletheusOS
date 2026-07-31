from aletheus.tooling.kinekt.orchestration.planner import build_units


def test_work_packages_become_execution_units() -> None:
    roadmap = {
        "work_packages": [
            {
                "package_id": "wp-ownership",
                "title": "Ownership Optimization",
                "phase": 1,
                "category": "ownership",
                "candidate_ids": ["normalize-ownership"],
                "estimated_effort": "high",
                "risk": "low",
                "expected_health_gain": 8.5,
            }
        ]
    }

    units, abstentions = build_units(roadmap)

    assert len(units) == 1
    assert units[0].unit_id == "eu-wp-ownership"
    assert abstentions == []
