from aletheus.tooling.production_consciousness.engine import Engine


def test_production_consciousness() -> None:
    report = Engine().synthesize(
        changed="x",
        reason="y",
        constitutional=True,
        safe=True,
        quality_delta=1,
        risk_delta=-1,
        recommendation="promote",
        evidence=("e",),
    )
    assert report["status"] == "self_explained"
