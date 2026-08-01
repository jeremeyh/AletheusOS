from aletheus.tooling.operational_excellence.engine import Engine


def test_operational_excellence() -> None:
    result = Engine().evaluate(
        deployability=100,
        rollback=100,
        backup=100,
        provenance=100,
        compatibility=100,
        recovery=100,
    )
    assert result.status == "operationally_certified"
