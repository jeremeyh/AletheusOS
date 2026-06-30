from aletheus.runtime import runtime_core


def test_executive_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Executive Intelligence Layer" in diagnostics["services"]


def test_executive_summary():
    result = runtime_core.commands.dispatch("executive.summary", {})
    assert not result.errors
    assert "summary" in result.results
    assert result.results["summary"]["title"] == "Aletheus Executive Summary"


def test_executive_recommendations():
    result = runtime_core.commands.dispatch("executive.recommendations", {})
    assert not result.errors
    assert "recommendations" in result.results
    assert len(result.results["recommendations"]) >= 1


def test_executive_daily_brief():
    result = runtime_core.commands.dispatch("executive.daily_brief", {})
    assert not result.errors
    assert "brief" in result.results
    assert result.results["brief"]["title"] == "Founder Daily Brief"


if __name__ == "__main__":
    test_executive_service_registered()
    test_executive_summary()
    test_executive_recommendations()
    test_executive_daily_brief()
    print("Aletheus v1.2 Executive Intelligence Layer tests passed.")
