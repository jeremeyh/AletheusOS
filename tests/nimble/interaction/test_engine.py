from aletheus.nimble.interaction.engine import Engine


def test_interaction_catalog() -> None:
    assert {"Button", "Toggle", "Command"} <= {item.name for item in Engine().catalog()}
