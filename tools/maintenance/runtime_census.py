from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def safe_len(obj):
    if obj is None:
        return 0
    if hasattr(obj, "count") and callable(obj.count):
        return obj.count()
    if hasattr(obj, "services"):
        return len(obj.services)
    if hasattr(obj, "handlers"):
        return len(obj.handlers)
    if hasattr(obj, "commands"):
        return len(obj.commands)
    if hasattr(obj, "_services"):
        return len(obj._services)
    if hasattr(obj, "_handlers"):
        return len(obj._handlers)
    if hasattr(obj, "_commands"):
        return len(obj._commands)
    try:
        return len(obj)
    except Exception:
        return 0


def section(title):
    print()
    print(title)
    print("-" * len(title))


def main():
    from aletheus.runtime import runtime_core

    print("AletheusOS Runtime Census")
    print("=" * 40)

    runtime_core.boot()

    print(f"Runtime type: {type(runtime_core).__name__}")
    print(f"Runtime version: {getattr(runtime_core, 'version', 'unknown')}")
    print(f"Runtime status: {getattr(runtime_core, 'status', 'unknown')}")

    section("Registries")

    registries = {
        "commands": getattr(runtime_core, "commands", None),
        "services": getattr(runtime_core, "services", None),
        "engines": getattr(runtime_core, "engines", None),
        "pipelines": getattr(runtime_core, "pipelines", None),
        "workflows": getattr(runtime_core, "workflows", None),
        "events": getattr(runtime_core, "events", None),
        "metrics": getattr(runtime_core, "metrics", None),
        "scheduler": getattr(runtime_core, "scheduler", None),
        "job_queue": getattr(runtime_core, "job_queue", None),
    }

    for name, obj in registries.items():
        status = "FOUND" if obj is not None else "MISSING"
        print(f"{name:12} {status:8} {type(obj).__name__ if obj else ''} count={safe_len(obj)}")

    section("Runtime Self Commands")

    commands_to_test = [
        "runtime.diagnostics",
        "runtime.selftest",
        "runtime.dashboard",
        "runtime.snapshot",
        "runtime.audit",
        "runtime.doctor",
        "runtime.invariants",
        "runtime.boot.validate",
        "runtime.health_report",
        "runtime.metrics",
        "runtime.events",
        "runtime.queue",
        "runtime.health",
    ]

    command_bus = getattr(runtime_core, "commands", None)

    passed = 0
    failed = 0

    for command in commands_to_test:
        try:
            ctx = command_bus.dispatch(command)
            if getattr(ctx, "errors", None):
                failed += 1
                print(f"FAIL {command}")
                for error in ctx.errors[:2]:
                    print(f"  {error}")
            else:
                passed += 1
                print(f"PASS {command}")
        except Exception as exc:
            failed += 1
            print(f"FAIL {command}")
            print(f"  {type(exc).__name__}: {exc}")

    section("Inspector")

    try:
        from aletheus.runtime.inspector import RuntimeInspector

        inspector = RuntimeInspector(runtime_core)
        print(f"summary: {inspector.summary()}")
        print(f"handlers: {len(inspector.handlers())}")
        print(f"services: {len(inspector.services())}")
    except Exception as exc:
        print(f"Inspector failed: {type(exc).__name__}: {exc}")

    section("Overall")

    print(f"Runtime command checks passed: {passed}")
    print(f"Runtime command checks failed: {failed}")

    if failed:
        print("OVERALL: WARN")
        raise SystemExit(1)

    print("OVERALL: PASS")


if __name__ == "__main__":
    main()
