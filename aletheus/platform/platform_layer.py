from __future__ import annotations

import json
import os
import platform
import shutil
import sys
from pathlib import Path

from aletheus.time_utils import utc_now_iso


class PlatformLayer:
    """
    AletheusOS Platform Layer™

    Abstracts the machine/runtime environment beneath AletheusOS.
    """

    VERSION = "1.0.1"

    REQUIRED_DIRS = [
        "aletheus",
        "cardhawk",
        "tools",
        "reports",
        "runtime_state",
    ]

    REQUIRED_TOOLS = [
        "python3",
    ]

    OPTIONAL_TOOLS = [
        "git",
        "pip",
        "streamlit",
    ]

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.report_dir = self.root / "reports" / "platform"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self):
        checks = {
            "system": self._system_info(),
            "python": self._python_info(),
            "filesystem": self._filesystem_info(),
            "directories": self._directory_checks(),
            "tools": self._tool_checks(),
            "environment": self._environment_checks(),
        }

        findings = self._findings(checks)

        score = 100

        for finding in findings:
            if finding["severity"] == "critical":
                score -= 30
            elif finding["severity"] == "high":
                score -= 15
            elif finding["severity"] == "medium":
                score -= 7
            elif finding["severity"] == "low":
                score -= 2

        score = max(score, 0)

        status = "healthy"
        if any(f["severity"] == "critical" for f in findings):
            status = "critical"
        elif any(f["severity"] == "high" for f in findings):
            status = "degraded"
        elif findings:
            status = "watching"

        result = {
            "platform": {
                "version": self.VERSION,
                "timestamp": utc_now_iso(),
                "root": str(self.root),
                "status": status,
                "score": score,
                "checks": checks,
                "findings": findings,
            }
        }

        self._write_reports(result)
        return result

    def _system_info(self):
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "platform": platform.platform(),
            "hostname": platform.node(),
        }

    def _python_info(self):
        """
        Robust virtual environment detection.

        Works with:
        • venv
        • virtualenv
        • Homebrew Python
        • Apple Silicon
        """

        virtual_env = os.environ.get("VIRTUAL_ENV")

        venv_active = (
            virtual_env is not None
            or hasattr(sys, "real_prefix")
            or sys.prefix != getattr(sys, "base_prefix", sys.prefix)
        )

        return {
            "executable": sys.executable,
            "version": sys.version,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro,
            },
            "prefix": sys.prefix,
            "base_prefix": getattr(sys, "base_prefix", sys.prefix),
            "virtual_env": virtual_env,
            "virtualenv_active": venv_active,
            "path_entries": sys.path[:10],
        }

    def _filesystem_info(self):
        usage = shutil.disk_usage(self.root)

        return {
            "root_exists": self.root.exists(),
            "root_is_dir": self.root.is_dir(),
            "cwd": os.getcwd(),
            "disk_total_gb": round(usage.total / 1024**3, 2),
            "disk_used_gb": round(usage.used / 1024**3, 2),
            "disk_free_gb": round(usage.free / 1024**3, 2),
        }

    def _directory_checks(self):
        checks = []

        for directory in self.REQUIRED_DIRS:
            path = self.root / directory
            checks.append({
                "name": directory,
                "exists": path.exists(),
                "is_dir": path.is_dir(),
            })

        return checks

    def _tool_checks(self):
        return {
            "required": [
                {
                    "tool": tool,
                    "available": shutil.which(tool) is not None,
                }
                for tool in self.REQUIRED_TOOLS
            ],
            "optional": [
                {
                    "tool": tool,
                    "available": shutil.which(tool) is not None,
                }
                for tool in self.OPTIONAL_TOOLS
            ],
        }

    def _environment_checks(self):
        return {
            "env_count": len(os.environ),
            "sensitive_env_names_detected": [
                key
                for key in os.environ
                if any(
                    token in key.upper()
                    for token in [
                        "TOKEN",
                        "SECRET",
                        "PASSWORD",
                        "KEY",
                        "CREDENTIAL",
                    ]
                )
            ],
        }

    def _findings(self, checks):
        findings = []

        if not checks["python"]["virtualenv_active"]:
            findings.append({
                "severity": "medium",
                "code": "VENV_NOT_ACTIVE",
                "message": "Python virtual environment does not appear to be active.",
            })

        return findings

    def _write_reports(self, result):
        json_path = self.report_dir / "platform_report.json"
        md_path = self.report_dir / "platform_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

        md_path.write_text(
            "\n".join([
                "# AletheusOS Platform Layer Report",
                "",
                f"Generated: {result['platform']['timestamp']}",
                f"Status: **{result['platform']['status']}**",
                f"Score: **{result['platform']['score']}**",
                f"Root: `{result['platform']['root']}`",
                "",
                "## Python",
                "",
                f"- executable: `{result['platform']['checks']['python']['executable']}`",
                f"- virtualenv_active: `{result['platform']['checks']['python']['virtualenv_active']}`",
                f"- virtual_env: `{result['platform']['checks']['python']['virtual_env']}`",
            ]),
            encoding="utf-8",
        )
