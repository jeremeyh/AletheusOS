from aletheus.runtime import runtime_core


def test_prediction_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Predictive Intelligence Layer" in diagnostics["services"]


def test_forecast_generation():
    result = runtime_core.commands.dispatch(
        "predict.forecast", {"horizon": "next sprint"}
    )
    assert not result.errors, result.errors
    assert "forecast" in result.results
    assert result.results["forecast"]["confidence"] > 0


def test_scenario_generation():
    result = runtime_core.commands.dispatch(
        "predict.scenario",
        {
            "title": "Marketplace Integration",
            "premise": "Card Hawk Marketplace Intelligence becomes a native application service.",
        },
    )
    assert not result.errors, result.errors
    assert "scenario" in result.results
    assert result.results["scenario"]["confidence"] > 0


def test_risks_and_opportunities():
    risks = runtime_core.commands.dispatch("predict.risks", {})
    opportunities = runtime_core.commands.dispatch("predict.opportunities", {})

    assert not risks.errors, risks.errors
    assert not opportunities.errors, opportunities.errors
    assert "risks" in risks.results
    assert "opportunities" in opportunities.results


def test_predictive_recommendations():
    result = runtime_core.commands.dispatch("predict.recommend", {})
    assert not result.errors, result.errors
    assert "recommendations" in result.results
    assert len(result.results["recommendations"]) >= 1


if __name__ == "__main__":
    test_prediction_service_registered()
    test_forecast_generation()
    test_scenario_generation()
    test_risks_and_opportunities()
    test_predictive_recommendations()
    print("Aletheus v1.7 Predictive Intelligence Layer tests passed.")
