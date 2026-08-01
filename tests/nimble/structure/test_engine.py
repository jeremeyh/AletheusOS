from aletheus.nimble.structure.engine import Engine


def test_structure_catalog() -> None:
    assert {"Surface", "Grid", "Stack"} <= {item.name for item in Engine().catalog()}
