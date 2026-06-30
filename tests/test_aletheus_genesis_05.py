from aletheus.runtime import runtime_core


def test_cognition_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Cognition Core" in diagnostics["services"]


def test_goal_create_and_list():
    created = runtime_core.commands.dispatch(
        "goal.create",
        {
            "title": "Test Goal",
            "description": "Validate Cognition Core.",
            "priority": "high",
            "application": "tests",
        },
    )

    assert not created.errors
    assert "goal" in created.results

    listed = runtime_core.commands.dispatch("goal.list", {})
    assert not listed.errors
    assert len(listed.results["goals"]) >= 1


def test_plan_generate():
    result = runtime_core.commands.dispatch(
        "plan.generate",
        {
            "goal_id": "test",
            "goal_title": "Increase Card Hawk portfolio value",
        },
    )

    assert not result.errors
    assert "plan" in result.results
    assert len(result.results["plan"]["steps"]) >= 1


def test_reason_evaluate():
    result = runtime_core.commands.dispatch(
        "reason.evaluate",
        {
            "prompt": "Should we prioritize marketplace intelligence?",
            "evidence": ["It improves scoring", "It improves timing"],
            "assumptions": ["Data is incomplete"],
        },
    )

    assert not result.errors
    assert "reasoning" in result.results
    assert result.results["reasoning"]["confidence"] > 0


def test_decision_record():
    result = runtime_core.commands.dispatch(
        "decision.record",
        {
            "title": "Test Decision",
            "decision": "Proceed",
            "rationale": "Cognition Core test decision.",
            "confidence": 0.9,
            "evidence": ["Test evidence"],
        },
    )

    assert not result.errors
    assert "decision" in result.results


if __name__ == "__main__":
    test_cognition_service_registered()
    test_goal_create_and_list()
    test_plan_generate()
    test_reason_evaluate()
    test_decision_record()
    print("Aletheus Genesis 0.5 Cognition Core tests passed.")
