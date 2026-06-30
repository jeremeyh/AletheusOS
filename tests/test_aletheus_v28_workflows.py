from aletheus.runtime import runtime_core


def test_workflow_service_registered():
    ctx = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = ctx.results["diagnostics"]
    assert "Aletheus Workflow Intelligence Engine" in diagnostics["services"]


def test_workflow_bootstrap():
    result = runtime_core.commands.dispatch("workflow.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["workflow"]["workflows"] >= 1


def test_create_start_pause_resume_cancel():
    created = runtime_core.commands.dispatch(
        "workflow.create",
        {
            "title": "Card Hawk Purchase Pipeline",
            "description": "Research → Marketplace → Decision",
        },
    )

    assert not created.errors, created.errors

    workflow = created.results["workflow"]

    workflow_id = workflow["workflow_id"]

    started = runtime_core.commands.dispatch(
        "workflow.start",
        {"workflow_id": workflow_id},
    )

    assert started.results["workflow"]["status"] == "running"

    paused = runtime_core.commands.dispatch(
        "workflow.pause",
        {"workflow_id": workflow_id},
    )

    assert paused.results["workflow"]["status"] == "paused"

    resumed = runtime_core.commands.dispatch(
        "workflow.resume",
        {"workflow_id": workflow_id},
    )

    assert resumed.results["workflow"]["status"] == "running"

    cancelled = runtime_core.commands.dispatch(
        "workflow.cancel",
        {"workflow_id": workflow_id},
    )

    assert cancelled.results["workflow"]["status"] == "cancelled"


def test_statistics():

    stats = runtime_core.commands.dispatch(
        "workflow.statistics",
        {},
    )

    assert not stats.errors
    assert "workflow_stats" in stats.results


if __name__ == "__main__":

    test_workflow_service_registered()
    test_workflow_bootstrap()
    test_create_start_pause_resume_cancel()
    test_statistics()

    print("Aletheus v2.8 Workflow Intelligence tests passed.")
