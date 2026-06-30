from pathlib import Path
from aletheus.runtime import runtime_core


def test_selftest():
    ctx = runtime_core.commands.dispatch("runtime.selftest", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["selftest"]["status"] == "pass"


def test_dashboard():
    ctx = runtime_core.commands.dispatch("runtime.dashboard", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["dashboard"]["health"] == "pass"


def test_snapshot():
    ctx = runtime_core.commands.dispatch("runtime.snapshot", {})
    assert not ctx.errors, ctx.errors
    snapshot = ctx.results["snapshot"]
    assert "commands" in snapshot
    assert "compatibility" in snapshot
    assert "kernel" in snapshot


def test_audit():
    ctx = runtime_core.commands.dispatch("runtime.audit", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["audit"]["health"] in ("healthy", "warning")


def test_docs():
    path = "RUNTIME_DOCUMENTATION.md"
    ctx = runtime_core.commands.dispatch("runtime.docs", {"path": path})
    assert not ctx.errors, ctx.errors
    assert ctx.results["documentation"]["status"] == "written"
    assert Path(path).exists()


if __name__ == "__main__":
    test_selftest()
    test_dashboard()
    test_snapshot()
    test_audit()
    test_docs()

    print("\n✔ AletheusOS v4.1.1 Engineering Foundation tests passed.")
