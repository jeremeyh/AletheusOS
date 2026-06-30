from aletheus.runtime import runtime_core


def test_uil_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Universal Intelligence Layer" in diagnostics["services"]


def test_uil_context():
    result = runtime_core.commands.dispatch(
        "uil.context",
        {"question": "What is Aletheus state?"},
    )
    assert not result.errors
    assert "context" in result.results


def test_uil_reason():
    result = runtime_core.commands.dispatch(
        "uil.reason",
        {"question": "What should Aletheus do next?"},
    )
    assert not result.errors
    assert "reasoning" in result.results
    assert result.results["reasoning"]["confidence"] > 0


def test_uil_decide():
    result = runtime_core.commands.dispatch(
        "uil.decide",
        {"question": "What should Card Hawk Foundation prioritize next?"},
    )
    assert not result.errors
    assert "decision" in result.results
    assert result.results["decision"]["confidence"] > 0


def test_uil_brief():
    result = runtime_core.commands.dispatch("uil.brief", {})
    assert not result.errors
    assert "brief" in result.results


if __name__ == "__main__":
    test_uil_service_registered()
    test_uil_context()
    test_uil_reason()
    test_uil_decide()
    test_uil_brief()
    print("Aletheus v1.6 Universal Intelligence Layer tests passed.")
