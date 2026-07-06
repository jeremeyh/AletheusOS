"""
AletheusOS

Genesis 53.4

Proof 001

Runtime Boot Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.runtime.core import AletheusRuntime


def header(title: str) -> None:
    print()
    print(title)
    print("=" * len(title))


def main() -> None:
    runtime = AletheusRuntime()

    header("RUNTIME BOOT")

    result = {
        "version": runtime.version,
        "status": runtime.status,
        "commands": runtime.commands.count(),
        "services": runtime.services.count(),
        "engines": runtime.engines.count(),
        "has_registration_manager": hasattr(runtime, "registration_manager"),
        "has_runtime_inspector": hasattr(runtime, "runtime_inspector"),
        "has_lifecycle_manager": hasattr(runtime, "lifecycle_manager"),
    }

    pprint(result)

    assert runtime.status in {"online", "READY"}
    assert runtime.commands.count() > 0
    assert runtime.services.count() > 0
    assert hasattr(runtime, "registration_manager")
    assert hasattr(runtime, "runtime_inspector")
    assert hasattr(runtime, "lifecycle_manager")

    header("INSPECTOR SUMMARY")
    pprint(runtime.runtime_inspector.summary())

    header("REGISTRATION MANAGER")
    pprint(runtime.registration_manager.statistics())

    header("LIFECYCLE MANAGER")
    pprint(runtime.lifecycle_manager.statistics())

    header("BOOT PROOF PASSED")


if __name__ == "__main__":
    main()
