from aletheus.nimble.engine_instruments.engine import Engine


def test_engine_instruments() -> None:
    names = {item.name for item in Engine().catalog()}
    assert "EvidenceEngine" in names and "PredictiveEngine" in names
