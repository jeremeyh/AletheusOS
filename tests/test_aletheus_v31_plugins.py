from aletheus.runtime import runtime_core


def test_plugin_service_registered():
    ctx = runtime_core.commands.dispatch("runtime.diagnostics")
    diagnostics = ctx.results["diagnostics"]
    assert "Aletheus Plugin Manager" in diagnostics["services"]


def test_plugin_bootstrap():
    result = runtime_core.commands.dispatch("plugin.bootstrap", {})
    assert not result.errors, result.errors
    assert result.results["plugin"]["plugins"] >= 1


def test_plugin_lifecycle():

    installed = runtime_core.commands.dispatch(
        "plugin.install",
        {
            "name": "Sample Plugin",
            "version": "1.0.0",
        },
    )

    assert not installed.errors, installed.errors

    plugin = installed.results["plugin"]
    plugin_id = plugin["plugin_id"]

    enabled = runtime_core.commands.dispatch(
        "plugin.enable",
        {"plugin_id": plugin_id},
    )

    assert not enabled.errors

    disabled = runtime_core.commands.dispatch(
        "plugin.disable",
        {"plugin_id": plugin_id},
    )

    assert not disabled.errors

    removed = runtime_core.commands.dispatch(
        "plugin.remove",
        {"plugin_id": plugin_id},
    )

    assert not removed.errors


def test_plugin_statistics():

    stats = runtime_core.commands.dispatch(
        "plugin.statistics",
        {},
    )

    assert not stats.errors
    assert "plugin_stats" in stats.results


if __name__ == "__main__":
    test_plugin_service_registered()
    test_plugin_bootstrap()
    test_plugin_lifecycle()
    test_plugin_statistics()

    print("✔ AletheusOS v3.1 Plugin Framework tests passed.")
