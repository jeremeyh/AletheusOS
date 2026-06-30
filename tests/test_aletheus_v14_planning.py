from aletheus.runtime import runtime_core


def test_planning_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Autonomous Planning Engine" in diagnostics["services"]


def test_create_plan():
    result = runtime_core.commands.dispatch(
        "planning.create",
        {"objective": "Validate autonomous planning engine."},
    )
    assert not result.errors
    assert "plan" in result.results
    assert len(result.results["plan"]["steps"]) >= 1


def test_execute_next_step():
    created = runtime_core.commands.dispatch(
        "planning.create",
        {"objective": "Prepare Card Hawk Foundation for native Aletheus operation."},
    )
    plan = created.results["plan"]

    executed = runtime_core.commands.dispatch(
        "planning.execute_next",
        {"plan_id": plan["plan_id"]},
    )

    assert not executed.errors
    assert "execution" in executed.results
    assert executed.results["execution"]["executed_step"]["status"] == "completed"


def test_execute_full_plan():
    created = runtime_core.commands.dispatch(
        "planning.create",
        {"objective": "Validate full autonomous plan execution."},
    )
    plan = created.results["plan"]

    executed = runtime_core.commands.dispatch(
        "planning.execute",
        {"plan_id": plan["plan_id"]},
    )

    assert not executed.errors
    assert executed.results["execution"]["final_plan"]["status"] == "completed"


if __name__ == "__main__":
    test_planning_service_registered()
    test_create_plan()
    test_execute_next_step()
    test_execute_full_plan()
    print("Aletheus v1.4 Autonomous Planning Engine tests passed.")
