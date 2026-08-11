from aletheus.runtime import runtime_core


def test_semantic_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Semantic Intelligence Layer" in diagnostics["services"]


def test_create_concept_and_assertion():
    concept = runtime_core.commands.dispatch(
        "semantic.concept.create",
        {
            "name": "Caleb Williams",
            "concept_type": "player",
            "description": "Chicago Bears quarterback.",
        },
    )
    assert not concept.errors
    assert concept.results["concept"]["name"] == "Caleb Williams"

    assertion = runtime_core.commands.dispatch(
        "semantic.assert",
        {
            "subject": "Caleb Williams",
            "predicate": "plays_for",
            "object_value": "Chicago Bears",
            "confidence": 0.9,
        },
    )
    assert not assertion.errors
    assert assertion.results["assertion"]["predicate"] == "plays_for"


def test_semantic_explain():
    result = runtime_core.commands.dispatch(
        "semantic.explain", {"name": "Caleb Williams"}
    )
    assert not result.errors
    assert "explanation" in result.results


def test_cardhawk_semantic_bootstrap():
    result = runtime_core.commands.dispatch("semantic.bootstrap.cardhawk", {})
    assert not result.errors
    assert "bootstrap" in result.results
    assert len(result.results["bootstrap"]["concepts"]) >= 1


if __name__ == "__main__":
    test_semantic_service_registered()
    test_create_concept_and_assertion()
    test_semantic_explain()
    test_cardhawk_semantic_bootstrap()
    print("Aletheus v1.1 Semantic Intelligence Layer tests passed.")
