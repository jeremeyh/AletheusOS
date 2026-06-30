from aletheus.runtime import runtime_core


def test_persistence_service_registered():
    ctx = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = ctx.results["diagnostics"]

    assert "Aletheus Persistence Engine" in diagnostics["services"]


def test_state_bootstrap():

    result = runtime_core.commands.dispatch(
        "state.bootstrap",
        {},
    )

    assert not result.errors, result.errors

    state = result.results["state"]

    assert state["health"] == "healthy"


def test_save_load():

    saved = runtime_core.commands.dispatch(
        "state.save",
        {},
    )

    assert not saved.errors, saved.errors

    loaded = runtime_core.commands.dispatch(
        "state.load",
        {},
    )

    assert not loaded.errors, loaded.errors

    assert loaded.results["state"]["loaded"] is True


def test_snapshot_restore():

    snapshot = runtime_core.commands.dispatch(
        "state.snapshot",
        {
            "name": "Regression Snapshot",
        },
    )

    assert not snapshot.errors, snapshot.errors

    snapshot_id = snapshot.results["snapshot"]["snapshot_id"]

    restored = runtime_core.commands.dispatch(
        "state.restore",
        {
            "snapshot_id": snapshot_id,
        },
    )

    assert not restored.errors, restored.errors

    assert restored.results["state"]["restored"] is True


def test_export_import():

    exported = runtime_core.commands.dispatch(
        "state.export",
        {},
    )

    assert not exported.errors

    imported = runtime_core.commands.dispatch(
        "state.import",
        {
            "state": exported.results["state"]["state"],
        },
    )

    assert not imported.errors


def test_statistics():

    stats = runtime_core.commands.dispatch(
        "state.statistics",
        {},
    )

    assert not stats.errors

    assert "state_stats" in stats.results


if __name__ == "__main__":

    test_persistence_service_registered()
    test_state_bootstrap()
    test_save_load()
    test_snapshot_restore()
    test_export_import()
    test_statistics()

    print("\n✔ AletheusOS v3.2 Persistence Engine tests passed.")
