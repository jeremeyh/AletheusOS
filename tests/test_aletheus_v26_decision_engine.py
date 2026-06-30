from aletheus.runtime import runtime_core


def test_decision_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Autonomous Decision Engine" in diagnostics["services"]


def test_decision_bootstrap():
    result = runtime_core.commands.dispatch("decision.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["decision"]["policies"] >= 1


def test_decision_evaluate_execute_explain_rollback():
    runtime_core.commands.dispatch("reason.bootstrap", {})

    evaluated = runtime_core.commands.dispatch(
        "decision.evaluate",
        {
            "title": "Card Hawk Acquisition Decision",
            "objective": "Choose the best Card Hawk acquisition action.",
            "policy": "maximize_value",
            "options": [
                {
                    "title": "Buy undervalued Caleb Williams card",
                    "description": "High upside collectible asset.",
                    "value_score": 0.9,
                    "risk_score": 0.35,
                    "confidence": 0.82,
                    "cost_score": 0.72,
                    "speed_score": 0.8,
                },
                {
                    "title": "Wait for more comps",
                    "description": "Lower risk, slower execution.",
                    "value_score": 0.6,
                    "risk_score": 0.2,
                    "confidence": 0.7,
                    "cost_score": 0.95,
                    "speed_score": 0.4,
                },
            ],
        },
    )

    assert not evaluated.errors, evaluated.errors
    decision = evaluated.results["decision"]
    assert decision["selected_option"]["title"] == "Buy undervalued Caleb Williams card"

    executed = runtime_core.commands.dispatch(
        "decision.execute",
        {"decision_id": decision["decision_id"]},
    )
    assert not executed.errors, executed.errors
    assert executed.results["decision"]["status"] == "executed"

    explained = runtime_core.commands.dispatch(
        "decision.explain",
        {"decision_id": decision["decision_id"]},
    )
    assert not explained.errors, explained.errors
    assert "explanation" in explained.results

    rolled_back = runtime_core.commands.dispatch(
        "decision.rollback",
        {"decision_id": decision["decision_id"]},
    )
    assert not rolled_back.errors, rolled_back.errors
    assert rolled_back.results["decision"]["status"] == "rolled_back"


def test_decision_history_and_stats():
    history = runtime_core.commands.dispatch("decision.history", {})
    assert not history.errors, history.errors
    assert "history" in history.results

    stats = runtime_core.commands.dispatch("decision.statistics", {})
    assert not stats.errors, stats.errors
    assert "decision_stats" in stats.results


if __name__ == "__main__":
    test_decision_service_registered()
    test_decision_bootstrap()
    test_decision_evaluate_execute_explain_rollback()
    test_decision_history_and_stats()
    print("Aletheus v2.6 Autonomous Decision Engine tests passed.")
