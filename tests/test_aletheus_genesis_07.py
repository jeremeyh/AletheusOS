from aletheus.runtime import runtime_core


def test_mission_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Autonomous Mission Engine" in diagnostics["services"]


def test_create_mission():
    result = runtime_core.commands.dispatch(
        "mission.create",
        {
            "title": "Test Mission",
            "objective": "Validate Autonomous Mission Engine.",
            "application": "tests",
            "priority": "high",
            "tasks": [
                {"title": "Step One", "description": "First task."},
                {"title": "Step Two", "description": "Second task."},
            ],
        },
    )

    assert not result.errors
    assert "mission" in result.results
    assert len(result.results["mission"]["tasks"]) == 2


def test_generate_and_run_mission():
    created = runtime_core.commands.dispatch(
        "mission.from_goal",
        {
            "goal_title": "Increase Card Hawk portfolio value",
            "goal_description": "Validate generated mission.",
            "application": "tests",
        },
    )

    mission = created.results["mission"]

    run = runtime_core.commands.dispatch(
        "mission.run",
        {"mission_id": mission["mission_id"]},
    )

    assert not run.errors
    assert "mission_run" in run.results
    assert run.results["mission_run"]["status"] == "completed"


def test_mission_stats():
    stats = runtime_core.commands.dispatch("mission.stats", {})
    assert not stats.errors
    assert stats.results["mission_stats"]["missions"] >= 1


if __name__ == "__main__":
    test_mission_service_registered()
    test_create_mission()
    test_generate_and_run_mission()
    test_mission_stats()
    print("Aletheus Genesis 0.7 Autonomous Mission Engine tests passed.")
