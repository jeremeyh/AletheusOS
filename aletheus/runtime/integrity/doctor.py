from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from datetime import datetime
from pathlib import Path
from typing import Any, Dict
import json
import subprocess


def utc_now() -> str:
    return utc_now_iso()


class RuntimeDoctor:
    VERSION = "4.2.1"

    def __init__(self, runtime: Any):
        self.runtime = runtime

    def run(self) -> Dict[str, Any]:
        commands = self.runtime.commands.list()
        compat = self.runtime.compat.statistics()

        duplicate_commands = sorted(
            {c for c in commands if commands.count(c) > 1}
        )

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

        missing_aliases = [
            alias for alias in required_aliases
            if alias not in compat.get("aliases", [])
        ]

        checks = {
            "runtime_online": getattr(self.runtime, "status", None) == "online",
            "commands_registered": len(commands) > 0,
            "no_duplicate_commands": not duplicate_commands,
            "compatibility_registered": compat.get("registered", 0) >= 10,
            "required_aliases_present": not missing_aliases,
            "kernel_available": hasattr(self.runtime, "kernel"),
            "hardening_available": hasattr(self.runtime, "hardening"),
        }

        failed = [
            name for name, passed in checks.items()
            if not passed
        ]

        report = {
            "version": self.VERSION,
            "timestamp": utc_now(),
            "runtime_version": getattr(self.runtime, "version", "unknown"),
            "status": "pass" if not failed else "fail",
            "checks": checks,
            "failed": failed,
            "commands": len(commands),
            "duplicate_commands": duplicate_commands,
            "compatibility": compat,
            "missing_aliases": missing_aliases,
        }

        return report

    def write_reports(self) -> Dict[str, Any]:
        Path("reports").mkdir(exist_ok=True)

        report = self.run()

        json_path = Path("reports/runtime-health.json")
        md_path = Path("reports/runtime-health.md")

        json_path.write_text(json.dumps(report, indent=2))

        lines = [
            "# AletheusOS Runtime Health",
            "",
            f"Generated: {report['timestamp']}",
            f"Runtime Version: {report['runtime_version']}",
            f"Status: {report['status']}",
            "",
            "## Checks",
        ]

        for name, passed in report["checks"].items():
            marker = "PASS" if passed else "FAIL"
            lines.append(f"- {marker}: {name}")

        md_path.write_text("\\n".join(lines) + "\\n")

        return {
            "json": str(json_path),
            "markdown": str(md_path),
            "status": report["status"],
        }
