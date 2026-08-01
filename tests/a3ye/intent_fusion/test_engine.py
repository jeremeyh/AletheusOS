from aletheus.a3ye.intent_fusion.engine import Engine
from aletheus.a3ye.intent_fusion.models import GovernedEvidence


def test_x() -> None:
    evidence = (GovernedEvidence("e", "text", {}, (), 0.9, 0.1),)
    assert len(Engine().fuse((1.0, 0.0), (0.0, 1.0), evidence=evidence).vector) == 4
