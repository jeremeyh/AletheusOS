from aletheus.tooling.autonomous_release_intelligence.engine import Engine


def test_release_intelligence() -> None:
    report = Engine().recommend(
        production_score=100,
        regression_confidence=100,
        compatibility=100,
        rollback_confidence=100,
    )
    assert report["decision"] == "promote"
