from aletheus.runtime import runtime_core


def test_registry_initialized():
    assert hasattr(runtime_core, "compat")


def test_alias_registration():
    stats = runtime_core.compat.statistics()
    assert stats["registered"] >= 10
    assert stats["health"] == "healthy"


def test_alias_resolution():
    planning = runtime_core.compat.resolve("planning")
    workflow = runtime_core.compat.resolve("workflow")
    agents = runtime_core.compat.resolve("agents")

    assert planning is runtime_core.planning
    assert workflow is runtime_core.workflow
    assert agents is runtime_core.agents


def test_compat_commands():
    ctx = runtime_core.commands.dispatch("compat.statistics", {})
    assert not ctx.errors
    assert ctx.results["compat_stats"]["health"] == "healthy"

    ctx = runtime_core.commands.dispatch("compat.resolve", {"alias": "planning"})
    assert not ctx.errors
    assert ctx.results["service"]["resolved"] is True

    ctx = runtime_core.commands.dispatch("compat.contract", {"alias": "workflow"})
    assert not ctx.errors
    assert ctx.results["contract"]["name"] == "workflow"


def test_kernel_still_executes():
    result = runtime_core.kernel.execute("runtime.diagnostics", {})
    assert result["status"] == "completed"
    assert result["errors"] == []
    assert "diagnostics" in result["result"]


if __name__ == "__main__":
    test_registry_initialized()
    test_alias_registration()
    test_alias_resolution()
    test_compat_commands()
    test_kernel_still_executes()

    print("\n✔ AletheusOS v4.1 Runtime Compatibility Layer tests passed.")
