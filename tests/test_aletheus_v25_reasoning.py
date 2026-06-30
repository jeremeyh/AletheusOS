from aletheus.runtime import runtime_core


def test_reasoning_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Cognitive Reasoning Engine" in diagnostics["services"]


def test_reasoning_bootstrap():
    result = runtime_core.commands.dispatch("reason.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["reasoning"]["rules"] >= 1


def test_reasoning_evaluate_decision_explain():
    runtime_core.commands.dispatch("knowledge.bootstrap.cardhawk", {})
    runtime_core.commands.dispatch(
        "memory.mesh.store",
        {
            "key": "reasoning_cardhawk_context",
            "value": "Card Hawk Foundation is the flagship native application for AletheusOS.",
            "namespace": "cardhawk",
            "tags": ["cardhawk", "reasoning"],
        },
    )

    evaluation = runtime_core.commands.dispatch(
        "reason.evaluate",
        {"question": "What is Card Hawk Foundation in AletheusOS?"},
    )
    assert not evaluation.errors, evaluation.errors
    assert evaluation.results["evaluation"]["confidence"] > 0

    trace_id = evaluation.results["evaluation"]["trace_id"]

    explanation = runtime_core.commands.dispatch("reason.explain", {"trace_id": trace_id})
    assert not explanation.errors, explanation.errors
    assert "explanation" in explanation.results

    decision = runtime_core.commands.dispatch(
        "reason.decision",
        {"question": "Should Card Hawk remain the flagship native app?"},
    )
    assert not decision.errors, decision.errors
    assert "decision" in decision.results


def test_reasoning_trace_and_confidence():
    trace = runtime_core.commands.dispatch("reason.trace", {})
    assert not trace.errors, trace.errors

    confidence = runtime_core.commands.dispatch("reason.confidence", {})
    assert not confidence.errors, confidence.errors


def test_reasoning_stats():
    result = runtime_core.commands.dispatch("reason.statistics", {})
    assert not result.errors, result.errors
    assert "reasoning_stats" in result.results


if __name__ == "__main__":
    test_reasoning_service_registered()
    test_reasoning_bootstrap()
    test_reasoning_evaluate_decision_explain()
    test_reasoning_trace_and_confidence()
    test_reasoning_stats()
    print("Aletheus v2.5 Cognitive Reasoning Engine tests passed.")
