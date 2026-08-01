from aletheus.tooling.unified_production_installer.engine import Engine


def test_unified_plan(tmp_path) -> None:
    report = Engine(tmp_path).plan("production")
    assert report["transactional"] is True
    assert report["rollback_mode"] == "all_or_nothing"
