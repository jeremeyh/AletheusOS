from aletheus.runtime import runtime_core


def test_copilot_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Founder Copilot" in diagnostics["services"]


def test_copilot_brief():
    result = runtime_core.commands.dispatch("copilot.brief", {})
    assert not result.errors
    assert "brief" in result.results


def test_copilot_ask():
    result = runtime_core.commands.dispatch(
        "copilot.ask",
        {"prompt": "What should I work on next?"},
    )
    assert not result.errors
    assert "exchange" in result.results
    assert result.results["exchange"]["response"]


def test_copilot_recommend():
    result = runtime_core.commands.dispatch("copilot.recommend", {})
    assert not result.errors
    assert "recommendations" in result.results


if __name__ == "__main__":
    test_copilot_service_registered()
    test_copilot_brief()
    test_copilot_ask()
    test_copilot_recommend()
    print("Aletheus v1.5 Founder Copilot tests passed.")
