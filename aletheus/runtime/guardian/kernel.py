from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# Resolve project root from: aletheus/runtime/guardian/kernel.py
ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / "aletheus" / "runtime"

# Keep maintenance execution isolated from full aletheus package bootstraps.
# This allows imports like guardian.*, conclave.*, and watch_tower.* to work
# without loading the full Aletheus runtime package tree.
for candidate in (ROOT, RUNTIME):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from .models import GuardianEvent
from conclave.engine import ConclaveEngine
from watch_tower.runtime.engine import WatchTowerEngine


class GuardianKernel:
    """
    Guardian Kernel™

    Coordinates:
    - Conclave™ defensive action inspection
    - Watch Tower™ structural integrity scanning
    - Principle X escalation flags

    This module intentionally avoids importing the full aletheus runtime package
    to prevent side-effect bootstraps during maintenance execution.
    """

    VERSION = "1.0.0"

    def __init__(self, root: str | Path = "."):
        self.root = Path(root).resolve()
        self.events: list[dict] = []
        self.report_dir = self.root / "reports" / "guardian"
        self.report_dir.mkdir(parents=True, exist_ok=True)

    def inspect(self, action: str, target: str = "", source: str = "manual") -> dict:
        conclave_result = self._run_conclave(action, target, source)
        conclave = conclave_result.get("conclave", {})

        event = GuardianEvent(
            source=source,
            action=action,
            target=target,
            risk=conclave.get("risk", "unknown"),
            allowed=conclave.get("allowed", True),
            conclave_status=conclave.get("classification", ""),
            watch_tower_requested=conclave.get("watch_tower_requested", False),
            principle_x_required=conclave.get("principle_x", False),
            created_at=datetime.utcnow().isoformat(),
        )

        watch_tower_result = None
        if event.watch_tower_requested:
            watch_tower_result = self._run_watch_tower_scan()

        result = {
            "guardian": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "event": event.to_dict(),
                "conclave": conclave,
                "watch_tower": watch_tower_result,
                "principle_x": self._principle_x_decision(event),
                "decision": self._decision(event),
            }
        }

        self.events.append(result["guardian"])
        self._write_report(result)
        return result

    def lockdown(self, reason: str = "manual") -> dict:
        conclave = self._run_conclave_lockdown(reason)
        watch_tower = self._run_watch_tower_scan()

        result = {
            "guardian": {
                "version": self.VERSION,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "lockdown",
                "reason": reason,
                "conclave": conclave.get("conclave", {}),
                "watch_tower": watch_tower,
                "principle_x": {
                    "required": True,
                    "mode": "preserve_integrity",
                    "message": "Principle X escalation active.",
                },
                "decision": {
                    "allowed": False,
                    "mode": "emergency_lockdown",
                    "message": "Guardian Kernel lockdown engaged.",
                },
            }
        }

        self.events.append(result["guardian"])
        self._write_report(result)
        return result

    def status(self) -> dict:
        return {
            "guardian": {
                "version": self.VERSION,
                "root": str(self.root),
                "events": len(self.events),
                "status": "online",
                "report_dir": str(self.report_dir),
            }
        }

    def _run_conclave(self, action: str, target: str, source: str) -> dict:
        engine = ConclaveEngine(self.root)
        return engine.protect(
            action=action,
            target=target,
            source=source,
        )

    def _run_conclave_lockdown(self, reason: str) -> dict:
        engine = ConclaveEngine(self.root)
        return engine.emergency_lockdown(reason=reason)

    def _run_watch_tower_scan(self) -> dict | None:
        engine = WatchTowerEngine(self.root)
        result = engine.scan()
        engine.write_reports()
        return result.get("watch_tower", result)

    def _principle_x_decision(self, event: GuardianEvent) -> dict:
        if event.principle_x_required or event.risk in {"critical", "high"}:
            return {
                "required": True,
                "mode": "integrity_supremacy",
                "message": "Principle X requires preservation over convenience.",
            }

        return {
            "required": False,
            "mode": "normal",
            "message": "No Principle X escalation required.",
        }

    def _decision(self, event: GuardianEvent) -> dict:
        if event.risk == "critical":
            return {
                "allowed": False,
                "mode": "block_and_scan",
                "message": "Critical event blocked. Watch Tower scan requested.",
            }

        if event.risk == "high":
            return {
                "allowed": False,
                "mode": "block_and_audit",
                "message": "High-risk event blocked and audited.",
            }

        if event.risk == "medium":
            return {
                "allowed": True,
                "mode": "allow_with_monitoring",
                "message": "Medium-risk event allowed only with monitoring.",
            }

        return {
            "allowed": True,
            "mode": "allow",
            "message": "Low-risk event allowed.",
        }

    def _write_report(self, result: dict) -> None:
        json_path = self.report_dir / "guardian_report.json"
        md_path = self.report_dir / "guardian_report.md"

        json_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        md_path.write_text(self._markdown(result), encoding="utf-8")

    def _markdown(self, result: dict) -> str:
        guardian = result["guardian"]
        decision = guardian.get("decision", {})

        lines = [
            "# Guardian Kernel™ Report",
            "",
            f"Generated: {guardian.get('timestamp')}",
            f"Version: {guardian.get('version')}",
            "",
            "## Decision",
            "",
            f"- Allowed: {decision.get('allowed')}",
            f"- Mode: {decision.get('mode')}",
            f"- Message: {decision.get('message')}",
            "",
            "## Guardian Payload",
            "",
            "```json",
            json.dumps(guardian, indent=2),
            "```",
            "",
        ]

        return "\n".join(lines)
