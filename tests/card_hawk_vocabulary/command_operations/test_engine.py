from aletheus.card_hawk_vocabulary.command_operations.engine import Engine


def test_operations() -> None:
    assert Engine().resolve("Mission Control").canonical is True
