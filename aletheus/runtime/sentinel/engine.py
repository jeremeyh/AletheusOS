from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import SentinelFinding


class SentinelEngine:
    """
    Sentinel™
    Live runtime supervisor.

    Watches runtime services, records health, and requests Guardian /
    Watch Tower escalation when instability appears.
    """

    VERSION = "1.0.0"

    CORE_SERVICES = [
        "guardian",
        "conclave",
        "watch_tower",
        "aletheus_runtime",
        "cardhawk",
    ]

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.report_dir = self.root / "reports" / "sentinel"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.findings: list[SentinelFinding] = []

    def scan(self) -> dict:
        self.findings = []

        self._check_core_paths()
        self._check_reports()
        self._check_runtime_state()
        self._check_guardian_report()
        self._check_watch_tower_report()
        self._check_conclave_audit()

        result = self._result()
        self._write_reports(result)
        return result

    def heartbeat(self) -> dict:
        result = self.scan()
        sentinel = result["sentinel"]

        return {
            "sentinel": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "status": sentinel["status"],
                "score": sentinel["score"],
                "guardian_requested": sentinel["guardian_requested"],
                "watch_tower_requested": sentinel["watch_tower_requested"],
                "findings": sentinel["counts"],
            }
        }

    def _check_core_paths(self):
        required = {
            "guardian": self.root / "aletheus" / "runtime" / "guardian",
            "conclave": self.root / "aletheus" / "runtime" / "conclave",
            "watch_tower": self.root / "watch_tower",
            "aletheus_runtime": self.root / "aletheus" / "runtime",
            "cardhawk": self.root / "cardhawk",
        }

        for service, path in required.items():
            if not path.exists():
                self._finding(
                    service,
                    "offline",
                    "critical",
                    f"Required core service path missing: {path}",
                )

    def _check_reports(self):
        reports = self.root / "reports"
        if not reports.exists():
            self._finding(
                "reports",
                "missing",
                "medium",
                "Reports directory is missing.",
            )

    def _check_runtime_state(self):
        runtime_state = self.root / "runtime_state"
        if not runtime_state.exists():
            self._finding(
                "runtime_state",
                "missing",
                "medium",
                "runtime_state directory is missing.",
            )

    def _check_guardian_report(self):
        path = self.root / "reports" / "guardian" / "guardian_report.json"
        if not path.exists():
            self._finding(
                "guardian",
                "no_recent_report",
                "low",
                "Guardian report not found yet.",
            )

    def _check_watch_tower_report(self):
        path = self.root / "reports" / "watch_tower" / "watch_tower_report.json"
        if not path.exists():
            self._finding(
                "watch_tower",
                "no_recent_report",
                "low",
                "Watch Tower report not found yet.",
            )

    def _check_conclave_audit(self):
        path = self.root / "reports" / "conclave" / "conclave_audit.jsonl"
        if not path.exists():
            self._finding(
                "conclave",
                "no_audit_log",
                "low",
                "Conclave audit log not found yet.",
            )

    def _finding(self, service: str, status: str, severity: str, message: str):
        self.findings.append(
            SentinelFinding(
                service=service,
                status=status,
                severity=severity,
                message=message,
                created_at=datetime.utcnow().isoformat(),
            )
        )

    def _result(self) -> dict:
        counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for finding in self.findings:
            counts[finding.severity] = counts.get(finding.severity, 0) + 1

        score = 100
        score -= counts["critical"] * 30
        score -= counts["high"] * 15
        score -= counts["medium"] * 7
        score -= counts["low"] * 2
        score = max(score, 0)

        status = "healthy"
        if counts["critical"]:
            status = "critical"
        elif counts["high"]:
            status = "degraded"
        elif counts["medium"] or counts["low"]:
            status = "watching"

        return {
            "sentinel": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "root": str(self.root),
                "status": status,
                "score": score,
                "counts": counts,
                "guardian_requested": counts["critical"] > 0 or counts["high"] > 0,
                "watch_tower_requested": counts["critical"] > 0 or counts["medium"] > 0,
                "findings": [finding.to_dict() for finding in self.findings],
            }
        }

    def _write_reports(self, result: dict):
        json_path = self.report_dir / "sentinel_report.json"
        md_path = self.report_dir / "sentinel_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

    def _markdown(self, result: dict) -> str:
        sentinel = result["sentinel"]

        lines = [
            "# Sentinel™ Report",
            "",
            f"Generated: {sentinel['timestamp']}",
            f"Status: **{sentinel['status']}**",
            f"Score: **{sentinel['score']}**",
            "",
            "## Counts",
            "",
        ]

        for key, value in sentinel["counts"].items():
            lines.append(f"- {key}: {value}")

        lines.extend(["", "## Findings", ""])

        if not sentinel["findings"]:
            lines.append("- No findings.")
        else:
            for finding in sentinel["findings"]:
                lines.append(
                    f"- **[{finding['severity']}] {finding['service']}** — {finding['message']}"
                )

        return "\n".join(lines)
