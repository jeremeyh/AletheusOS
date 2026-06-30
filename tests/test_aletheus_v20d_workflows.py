from aletheus.runtime import runtime_core


def test_v2_workflow_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus v2 Autonomous Workflow Fabric" in diagnostics["services"]


def test_create_workflow():
    result = runtime_core.commands.dispatch(
        "workflow.v2.create",
        {
            "title": "Card Hawk Workflow Fabric Test",
            "objective": "Prepare Card Hawk Foundation for workflow-driven marketplace intelligence.",
            "application": "Card Hawk Foundation™",
        },
    )
    assert not result.errors, result.errors
    assert "workflow" in result.results
    assert len(result.results["workflow"]["nodes"]) >= 1


def test_execute_workflow():
    created = runtime_core.commands.dispatch(
        "workflow.v2.create",
        {
            "title": "Card Hawk Marketplace Workflow",
            "objective": "Coordinate Card Hawk marketplace readiness through workflow fabric.",
            "application": "Card Hawk Foundation™",
        },
    )
    workflow = created.results["workflow"]

    executed = runtime_core.commands.dispatch(
        "workflow.v2.execute",
        {"workflow_id": workflow["workflow_id"]},
    )

    assert not executed.errors, executed.errors
    assert "execution" in executed.results
    assert executed.results["execution"]["workflow"]["status"] in {"completed", "failed"}


def test_workflow_history():
    created = runtime_core.commands.dispatch(
        "workflow.v2.create",
        {
            "title": "Workflow History Test",
            "objective": "Validate workflow event history.",
            "application": "AletheusOS",
        },
    )
    workflow = created.results["workflow"]

    runtime_core.commands.dispatch(
        "workflow.v2.execute_next",
        {"workflow_id": workflow["workflow_id"]},
    )

    history = runtime_core.commands.dispatch(
        "workflow.v2.history",
        {"workflow_id": workflow["workflow_id"]},
    )

    assert not history.errors, history.errors
    assert "history" in history.results
    assert len(history.results["history"]) >= 1


def test_workflow_stats():
    result = runtime_core.commands.dispatch("workflow.v2.stats", {})
    assert not result.errors, result.errors
    assert "workflow_v2_stats" in result.results


if __name__ == "__main__":
    test_v2_workflow_service_registered()
    test_create_workflow()
    test_execute_workflow()
    test_workflow_history()
    test_workflow_stats()
    print("Aletheus v2.0D Autonomous Workflow Fabric tests passed.")
