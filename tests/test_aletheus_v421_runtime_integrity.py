from pathlib import Path
from aletheus.runtime import runtime_core


def test_runtime_doctor():
    ctx = runtime_core.commands.dispatch("runtime.doctor", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["doctor"]["status"] == "pass"


def test_runtime_invariants():
    ctx = runtime_core.commands.dispatch("runtime.invariants", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["invariants"]["status"] == "pass"


def test_boot_validator():
    ctx = runtime_core.commands.dispatch("runtime.boot.validate", {})
    assert not ctx.errors, ctx.errors
    assert ctx.results["boot_validation"]["status"] == "pass"


def test_health_report():
    ctx = runtime_core.commands.dispatch("runtime.health_report", {})
    assert not ctx.errors, ctx.errors

    report = ctx.results["health_report"]
    assert report["status"] == "pass"
    assert Path(report["json"]).exists()
    assert Path(report["markdown"]).exists()


if __name__ == "__main__":
    test_runtime_doctor()
    test_runtime_invariants()
    test_boot_validator()
    test_health_report()

    print("\\n✔ AletheusOS v4.2.1 Runtime Integrity tests passed.")
