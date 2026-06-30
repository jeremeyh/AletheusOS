from aletheus.runtime import runtime_core


def test_planning_service_registered():
    ctx = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = ctx.results["diagnostics"]
    assert "Aletheus Autonomous Planning Engine" in diagnostics["services"]


def test_planning_bootstrap():
    result = runtime_core.commands.dispatch("plan.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["planning"]["strategies"] >= 1


def test_plan_lifecycle():
    created = runtime_core.commands.dispatch(
        "plan.create",
        {"goal": "Acquire undervalued Card Hawk asset"},
    )
    assert not created.errors, created.errors

    plan = created.results["plan"]
    plan_id = plan["plan_id"]

    executed = runtime_core.commands.dispatch(
        "plan.execute",
        {"plan_id": plan_id},
    )
    assert not executed.errors, executed.errors
    assert executed.results["plan"]["status"] == "running"

    progress = runtime_core.commands.dispatch(
        "plan.progress",
        {"plan_id": plan_id},
    )
    assert not progress.errors, progress.errors
    assert "progress" in progress.results["plan"]

    replanned = runtime_core.commands.dispatch(
        "plan.replan",
        {"plan_id": plan_id},
    )
    assert not replanned.errors, replanned.errors
    assert replanned.results["plan"]["status"] == "replanned"

    completed = runtime_core.commands.dispatch(
        "plan.complete",
        {"plan_id": plan_id},
    )
    assert not completed.errors, completed.errors
    assert completed.results["plan"]["status"] == "completed"
    assert completed.results["plan"]["progress"] == 100.0


def test_plan_status_and_statistics():
    status = runtime_core.commands.dispatch("plan.status", {})
    assert not status.errors, status.errors
    assert "plans" in status.results

    stats = runtime_core.commands.dispatch("plan.statistics", {})
    assert not stats.errors, stats.errors
    assert "planning_stats" in stats.results


if __name__ == "__main__":
    test_planning_service_registered()
    test_planning_bootstrap()
    test_plan_lifecycle()
    test_plan_status_and_statistics()
    print("Aletheus v2.9 Autonomous Planning Engine tests passed.")
