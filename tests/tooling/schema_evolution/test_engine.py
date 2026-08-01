from aletheus.tooling.schema_evolution.engine import Engine, Migration


def test_schema_migration(tmp_path) -> None:
    engine = Engine(tmp_path)
    engine.register(
        Migration(
            "v1",
            0,
            1,
            lambda payload: {**payload, "ok": True},
        )
    )
    result = engine.migrate({"schema_version": 0}, 1)
    assert result["schema_version"] == 1
    assert result["ok"] is True
