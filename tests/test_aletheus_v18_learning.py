from aletheus.runtime import runtime_core


def test_learning_service_registered():
    context = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = context.results["diagnostics"]
    assert "Aletheus Adaptive Learning Engine" in diagnostics["services"]


def test_record_experience():
    result = runtime_core.commands.dispatch(
        "learn.record",
        {
            "event_type": "prediction",
            "description": "Validated predictive intelligence output.",
            "source": "tests",
            "outcome": "successful",
            "confidence": 0.9,
        },
    )
    assert not result.errors, result.errors
    assert "experience" in result.results


def test_create_lesson():
    result = runtime_core.commands.dispatch(
        "learn.lesson",
        {
            "title": "Test Lesson",
            "lesson": "Aletheus can capture explicit lessons.",
            "confidence": 0.85,
            "tags": ["test", "learning"],
        },
    )
    assert not result.errors, result.errors
    assert "lesson" in result.results


def test_patterns_and_improvements():
    patterns = runtime_core.commands.dispatch("learn.patterns", {})
    improvements = runtime_core.commands.dispatch("learn.improve", {})

    assert not patterns.errors, patterns.errors
    assert not improvements.errors, improvements.errors
    assert "patterns" in patterns.results
    assert "improvements" in improvements.results


def test_learning_snapshot():
    result = runtime_core.commands.dispatch("learn.snapshot", {})
    assert not result.errors, result.errors
    assert "snapshot" in result.results


if __name__ == "__main__":
    test_learning_service_registered()
    test_record_experience()
    test_create_lesson()
    test_patterns_and_improvements()
    test_learning_snapshot()
    print("Aletheus v1.8 Adaptive Learning Engine tests passed.")
