from aletheus.tooling.architectural_integrity.engine import Engine


def test_architectural_integrity() -> None:
    result = Engine().evaluate(
        boundaries=100,
        cycles=100,
        registry=100,
        authority=100,
        cohesion=100,
        constitutional_compliance=100,
    )
    assert result.status == "architecture_certified"
