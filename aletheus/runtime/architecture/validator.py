from __future__ import annotations

from typing import Any


class ArchitectureValidator:
    def __init__(self, runtime):

        self.runtime = runtime
        self.version = "1.0.0"

    def validate(self) -> dict[str, Any]:

        checks = {
            "registry_integrity": self._check_registry(),
            "command_integrity": self._check_commands(),
            "domain_integrity": self._check_domains(),
            "runtime_integrity": self._check_runtime(),
        }

        failures = [name for name, result in checks.items() if not result]

        return {
            "validator": "Architecture Validation Engine",
            "version": self.version,
            "healthy": len(failures) == 0,
            "checks": checks,
            "failures": failures,
        }

    def _check_registry(self):

        try:
            snapshot = self.runtime.registry_snapshot()

            return snapshot.get("healthy", False)

        except Exception:
            return False

    def _check_commands(self):

        try:
            audit = self.runtime.command_surface_audit()

            return audit.get("healthy", False)

        except Exception:
            return False

    def _check_domains(self):

        try:
            registry = self.runtime.registry_snapshot()

            return registry.get("domain_count", 0) > 0

        except Exception:
            return False

    def _check_runtime(self):

        return self.runtime is not None
