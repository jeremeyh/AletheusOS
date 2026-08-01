from aletheus.tooling.transaction_coordinator.engine import Engine


def test_transaction_commit(tmp_path) -> None:
    engine = Engine(tmp_path)
    transaction = engine.begin("t", ["a"])
    engine.checkpoint(transaction, "a", "c")
    report = engine.commit(transaction)
    assert report["status"] == "committed"
    assert report["rollback_mode"] == "all_or_nothing"
