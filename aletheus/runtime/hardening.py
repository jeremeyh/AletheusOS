from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.utcnow().isoformat()


class RuntimeHardening:
    VERSION = "4.1.1"

    def __init__(self, runtime):
        self.runtime = runtime

    def selftest(self) -> dict[str, Any]:
        checks = {}

        required_aliases = [
            "memory",
            "knowledge",
            "reasoning",
            "decision",
            "planning",
            "workflow",
            "agents",
            "security",
            "tenancy",
        ]

        for alias in required_aliases:
            try:
                self.runtime.compat.resolve(alias)
                checks[alias] = "pass"
            except Exception:
                checks[alias] = "fail"

        kernel_ok = all(
            hasattr(self.runtime, attr)
            for attr in [
                "intelligence_orchestrator",
                "intelligence_scheduler",
                "intelligence_dispatcher",
                "intelligence_supervisor",
            ]
        )

        checks["kernel"] = "pass" if kernel_ok else "fail"
        checks["compatibility"] = (
            "pass" if self.runtime.compat.statistics()["registered"] >= 10 else "fail"
        )

        status = "pass" if all(v == "pass" for v in checks.values()) else "fail"

        return {
            "version": self.VERSION,
            "status": status,
            "checks": checks,
            "timestamp": utc_now(),
        }

    def dashboard(self) -> dict[str, Any]:
        selftest = self.selftest()
        compat = self.runtime.compat.statistics()

        return {
            "runtime": {
                "version": self.runtime.version,
                "status": getattr(self.runtime, "status", "unknown"),
            },
            "health": selftest["status"],
            "services": compat,
            "checks": selftest["checks"],
            "timestamp": utc_now(),
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "timestamp": utc_now(),
            "runtime_version": self.runtime.version,
            "status": getattr(self.runtime, "status", "unknown"),
            "commands": sorted(self.runtime.commands.list()),
            "services": self.runtime.diagnostics.report().get("services", []),
            "compatibility": self.runtime.compat.statistics(),
            "kernel": {
                "orchestrator": self.runtime.intelligence_orchestrator.statistics(),
                "scheduler": self.runtime.intelligence_scheduler.statistics(),
                "dispatcher": self.runtime.intelligence_dispatcher.statistics(),
                "supervisor": self.runtime.intelligence_supervisor.statistics(),
            },
        }

    def audit(self) -> dict[str, Any]:
        commands = self.runtime.commands.list()
        duplicates = sorted({c for c in commands if commands.count(c) > 1})

        compat_aliases = list(self.runtime.compat.services.keys())
        duplicate_aliases = sorted(
            {a for a in compat_aliases if compat_aliases.count(a) > 1}
        )

        missing_handlers = []
        for command in commands:
            handler_name = "_cmd_" + command.replace(".", "_")
            if not hasattr(self.runtime, handler_name):
                # Not all legacy commands follow direct naming convention.
                continue

        return {
            "version": self.VERSION,
            "commands": len(commands),
            "duplicate_commands": duplicates,
            "compat_aliases": len(compat_aliases),
            "duplicate_aliases": duplicate_aliases,
            "missing_handlers": missing_handlers,
            "health": "healthy"
            if not duplicates and not duplicate_aliases
            else "warning",
        }

    def documentation(self) -> str:
        snapshot = self.snapshot()

        lines = [
            "# AletheusOS Runtime Documentation",
            "",
            f"Generated: {snapshot['timestamp']}",
            f"Runtime Version: {snapshot['runtime_version']}",
            "",
            "## Compatibility Aliases",
        ]

        for alias in snapshot["compatibility"]["aliases"]:
            lines.append(f"- {alias}")

        lines.extend(["", "## Commands"])

        for command in snapshot["commands"]:
            lines.append(f"- `{command}`")

        return "\n".join(lines) + "\n"

    def write_documentation(
        self, path: str = "RUNTIME_DOCUMENTATION.md"
    ) -> dict[str, Any]:
        content = self.documentation()
        Path(path).write_text(content)
        return {
            "path": path,
            "bytes": len(content.encode("utf-8")),
            "status": "written",
        }
