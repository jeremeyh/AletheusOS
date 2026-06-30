from aletheus.runtime import runtime_core


def test_v2_mission_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus v2 Autonomous Mission Engine" in diagnostics["services"]


def test_create_v2_mission():
    result = runtime_core.commands.dispatch(
        "mission.v2.create",
        {
            "title": "Card Hawk Marketplace Readiness",
            "objective": "Prepare Card Hawk Foundation for marketplace intelligence execution.",
            "application": "Card Hawk Foundation™",
            "priority": "critical",
        },
    )
    assert not result.errors, result.errors
    assert "mission" in result.results
    assert len(result.results["mission"]["tasks"]) >= 1


def test_plan_and_execute_v2_mission():
    created = runtime_core.commands.dispatch(
        "mission.v2.create",
        {
            "title": "Card Hawk Native App Mission",
            "objective": "Coordinate Card Hawk native applications through the v2 kernel.",
            "application": "Card Hawk Foundation™",
            "priority": "high",
        },
    )
    mission = created.results["mission"]

    planned = runtime_core.commands.dispatch(
        "mission.v2.plan",
        {"mission_id": mission["mission_id"]},
    )
    assert not planned.errors, planned.errors
    assert "planning" in planned.results

    executed = runtime_core.commands.dispatch(
        "mission.v2.execute",
        {"mission_id": mission["mission_id"]},
    )
    assert not executed.errors, executed.errors
    assert "execution" in executed.results
    assert executed.results["execution"]["mission"]["status"] == "completed"


def test_v2_mission_telemetry():
    created = runtime_core.commands.dispatch(
        "mission.v2.create",
        {
            "title": "Telemetry Test Mission",
            "objective": "Validate mission telemetry.",
            "application": "AletheusOS",
        },
    )
    mission = created.results["mission"]

    runtime_core.commands.dispatch("mission.v2.execute_next", {"mission_id": mission["mission_id"]})

    telemetry = runtime_core.commands.dispatch(
        "mission.v2.telemetry",
        {"mission_id": mission["mission_id"]},
    )

    assert not telemetry.errors, telemetry.errors
    assert "telemetry" in telemetry.results
    assert len(telemetry.results["telemetry"]) >= 1


def test_v2_mission_stats():
    result = runtime_core.commands.dispatch("mission.v2.stats", {})
    assert not result.errors, result.errors
    assert "mission_v2_stats" in result.results


if __name__ == "__main__":
    test_v2_mission_service_registered()
    test_create_v2_mission()
    test_plan_and_execute_v2_mission()
    test_v2_mission_telemetry()
    test_v2_mission_stats()
    print("Aletheus v2.0C Autonomous Mission Engine tests passed.")
