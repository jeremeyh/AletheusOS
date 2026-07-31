from __future__ import annotations

from typing import Any


class RuntimeBootValidator:
    VERSION = "4.2.1"

    def __init__(self, runtime: Any):
        self.runtime = runtime

    def validate(self) -> dict[str, Any]:
        checks = {
            "status_online": getattr(self.runtime, "status", None) == "online",
            "commands_registered": len(self.runtime.commands.list()) > 0,
            "compat_registered": self.runtime.compat.statistics().get("registered", 0)
            >= 10,
            "kernel_available": hasattr(self.runtime, "kernel"),
            "diagnostics_available": "runtime.diagnostics"
            in self.runtime.commands.list(),
        }

        failed = [name for name, passed in checks.items() if not passed]

        return {
            "version": self.VERSION,
            "status": "pass" if not failed else "fail",
            "checks": checks,
            "failed": failed,
        }
