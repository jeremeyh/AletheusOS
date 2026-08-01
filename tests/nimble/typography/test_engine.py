from aletheus.nimble.typography.engine import Engine


def test_typography_catalog() -> None:
    assert {"Display", "Heading", "Body"} <= {item.name for item in Engine().catalog()}
