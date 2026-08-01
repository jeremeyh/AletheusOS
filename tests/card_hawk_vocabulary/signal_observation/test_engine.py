from aletheus.card_hawk_vocabulary.signal_observation.engine import Engine


def test_signal() -> None:
    assert Engine().resolve("Radar").name == "Radar"
