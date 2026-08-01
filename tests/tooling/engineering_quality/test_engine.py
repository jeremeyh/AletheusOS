from aletheus.tooling.engineering_quality.engine import Engine


def test_engineering_quality() -> None:
    result = Engine().evaluate(
        lint=100,
        formatting=100,
        tests=100,
        coverage=100,
        complexity=100,
        maintainability=100,
    )
    assert result.status == "engineering_certified"
