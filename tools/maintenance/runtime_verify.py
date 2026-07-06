from __future__ import annotations

import importlib
import traceback
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class CheckResult:
    name: str
    status: str
    detail: str = ""


class RuntimeVerifier:
    def __init__(self):
        self.results: List[CheckResult] = []

    def check(self, name: str, fn: Callable[[], str | None]):
        try:
            detail = fn() or ""
            self.results.append(CheckResult(name, "PASS", detail))
        except Exception as exc:
            self.results.append(
                CheckResult(
                    name,
                    "FAIL",
                    f"{type(exc).__name__}: {exc}",
                )
            )

    def run(self):
        print("\nAletheusOS Runtime Verification")
        print("=" * 38)

        self.check("Import aletheus", self.check_import_aletheus)
        self.check("Import runtime", self.check_import_runtime)
        self.check("Runtime singleton", self.check_runtime_singleton)
        self.check("Runtime boot", self.check_runtime_boot)
        self.check("Command registry", self.check_command_registry)
        self.check("Core modules", self.check_core_modules)
        self.check("Advanced components", self.check_advanced_components)

        self.print_report()

    def check_import_aletheus(self):
        importlib.import_module("aletheus")
        return "aletheus imported"

    def check_import_runtime(self):
        runtime_module = importlib.import_module("aletheus.runtime")
        required = ["AletheusRuntime", "RuntimeContext", "runtime_core"]

        missing = [name for name in required if not hasattr(runtime_module, name)]
        if missing:
            raise RuntimeError(f"Missing runtime exports: {missing}")

        return "runtime exports available"

    def check_runtime_singleton(self):
        from aletheus.runtime import runtime_core

        if runtime_core is None:
            raise RuntimeError("runtime_core is None")

        return type(runtime_core).__name__

    def check_runtime_boot(self):
        from aletheus.runtime import runtime_core

        runtime_core.boot()
        return "boot completed"

    def check_command_registry(self):
        from aletheus.runtime import runtime_core

        commands = getattr(runtime_core, "commands", None)
        if commands is None:
            raise RuntimeError("runtime_core.commands missing")

        # Support multiple possible registry shapes safely.
        if hasattr(commands, "commands"):
            registry = commands.commands
        elif hasattr(commands, "_commands"):
            registry = commands._commands
        elif isinstance(commands, dict):
            registry = commands
        else:
            registry = None

        if registry is None:
            return f"commands object present: {type(commands).__name__}"

        count = len(registry)
        if count < 50:
            raise RuntimeError(f"Command count suspiciously low: {count}")

        return f"{count} commands detected"

    def check_core_modules(self):
        modules = [
            "aletheus.memory",
            "aletheus.cognition",
            "aletheus.knowledge",
            "aletheus.mission",
            "aletheus.workspace",
            "aletheus.applications",
            "aletheus.semantic",
            "aletheus.executive",
            "aletheus.agents",
            "aletheus.planning",
            "aletheus.copilot",
        ]

        loaded = []
        failed = []

        for module in modules:
            try:
                importlib.import_module(module)
                loaded.append(module)
            except Exception as exc:
                failed.append(f"{module}: {type(exc).__name__}: {exc}")

        if failed:
            raise RuntimeError("; ".join(failed))

        return f"{len(loaded)} core modules imported"

    def check_advanced_components(self):
        modules = [
            "aletheus.runtime.guardian",
            "aletheus.runtime.sentinel",
            "aletheus.runtime.conclave",
            "aletheus.atlas",
            "aletheus.council",
            "watch_tower",
        ]

        loaded = []
        missing = []

        for module in modules:
            try:
                importlib.import_module(module)
                loaded.append(module)
            except ModuleNotFoundError:
                missing.append(module)
            except Exception as exc:
                raise RuntimeError(f"{module}: {type(exc).__name__}: {exc}")

        detail = f"{len(loaded)} advanced components imported"
        if missing:
            detail += f"; missing/unavailable: {missing}"

        return detail

    def print_report(self):
        print()

        passed = 0
        failed = 0

        for result in self.results:
            symbol = "✓" if result.status == "PASS" else "✗"
            print(f"{symbol} {result.name}: {result.status}")
            if result.detail:
                print(f"  {result.detail}")

            if result.status == "PASS":
                passed += 1
            else:
                failed += 1

        print("\nSummary")
        print("-" * 38)
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")

        if failed:
            print("\nOVERALL: FAIL")
            raise SystemExit(1)

        print("\nOVERALL: PASS")


if __name__ == "__main__":
    RuntimeVerifier().run()
