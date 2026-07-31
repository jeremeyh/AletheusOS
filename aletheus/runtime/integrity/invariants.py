from __future__ import annotations

from typing import Any


class RuntimeInvariantEngine:
    VERSION = "4.2.1"

    def __init__(self, runtime: Any):
        self.runtime = runtime

    def validate(self) -> dict[str, Any]:
        checks: dict[str, bool] = {
            "runtime_version": bool(getattr(self.runtime, "version", "")),
            "command_bus": hasattr(self.runtime, "commands"),
            "event_bus": hasattr(self.runtime, "events"),
            "metrics": hasattr(self.runtime, "metrics"),
            "compatibility": hasattr(self.runtime, "compat"),
            "kernel": hasattr(self.runtime, "kernel"),
            "status_online": getattr(self.runtime, "status", None) == "online",
        }

        if hasattr(self.runtime, "compat"):
            checks["compatibility_aliases"] = (
                self.runtime.compat.statistics().get("registered", 0) >= 10
            )

        failed: list[str] = [name for name, passed in checks.items() if not passed]

        return {
            "version": self.VERSION,
            "status": "pass" if not failed else "fail",
            "checks": checks,
            "failed": failed,
        }
