from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

FILES = {
    "aletheus/runtime/guardian/__init__.py": '''"""
Guardian Kernel™
Coordinator for Conclave™, Watch Tower™, and Principle X.
"""

from .kernel import GuardianKernel

__all__ = ["GuardianKernel"]
''',

    "aletheus/runtime/guardian/models.py": '''from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class GuardianEvent:
    source: str
    action: str
    target: str = ""
    risk: str = "low"
    allowed: bool = True
    conclave_status: str = ""
    watch_tower_requested: bool = False
    principle_x_required: bool = False
    created_at: str = ""

    def to_dict(self):
        data = asdict(self)
        if not data["created_at"]:
            data["created_at"] = datetime.utcnow().isoformat()
        return data
''',

    "aletheus/runtime/guardian/kernel.py": '''from __future__ import annotations

import importlib.util
import json
from datetime import datetime
from pathlib import Path

from .models import GuardianEvent


class GuardianKernel:
    """
    Guardian Kernel™

    Coordinates:
    - Conclave™ defensive action inspection
    - Watch Tower™ structural integrity scanning
    - Principle X escalation flags

    This module intentionally avoids importing full aletheus runtime packages
    to prevent side-effect bootstraps during maintenance execution.
    """

    VERSION = "1.0.0"

    def __init__(self, root="."):
        self.root = Path(root).resolve()
        self.events = []
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
        module = self._load_module(
            "conclave_engine",
            self.root / "aletheus" / "runtime" / "conclave" / "engine.py",
        )
        engine = module.ConclaveEngine(self.root)
        return engine.protect(action=action, target=target, source=source)

    def _run_conclave_lockdown(self, reason: str) -> dict:
        module = self._load_module(
            "conclave_engine",
            self.root / "aletheus" / "runtime" / "conclave" / "engine.py",
        )
        engine = module.ConclaveEngine(self.root)
        return engine.emergency_lockdown(reason=reason)

    def _run_watch_tower_scan(self) -> dict | None:
        engine_path = self.root / "watch_tower" / "runtime" / "engine.py"

        if not engine_path.exists():
            return {
                "available": False,
                "message": "Watch Tower engine not found.",
            }

        module = self._load_module("watch_tower_engine", engine_path)
        engine = module.WatchTowerEngine(self.root)
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

    def _write_report(self, result: dict):
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

        return "\\n".join(lines)

    def _load_module(self, name: str, path: Path):
        spec = importlib.util.spec_from_file_location(name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module: {path}")

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
''',

    "tools/maintenance/run_guardian_kernel.py": '''import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_guardian_kernel():
    path = ROOT / "aletheus" / "runtime" / "guardian" / "kernel.py"
    spec = importlib.util.spec_from_file_location("guardian_kernel", path)

    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load Guardian Kernel: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.GuardianKernel


def main():
    parser = argparse.ArgumentParser(description="Guardian Kernel™ runner")
    parser.add_argument("--action", default="inspect")
    parser.add_argument("--target", default="")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--lockdown", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    GuardianKernel = load_guardian_kernel()
    kernel = GuardianKernel(ROOT)

    if args.status:
        result = kernel.status()
    elif args.lockdown:
        result = kernel.lockdown(reason=args.source)
    else:
        result = kernel.inspect(
            action=args.action,
            target=args.target,
            source=args.source,
        )

    if args.json:
        print(json.dumps(result, indent=2))
        return

    guardian = result["guardian"]
    decision = guardian.get("decision", {})

    print()
    print("=" * 72)
    print("Guardian Kernel™")
    print("=" * 72)
    print(f"Version : {guardian.get('version')}")
    print(f"Allowed : {decision.get('allowed')}")
    print(f"Mode    : {decision.get('mode', guardian.get('status'))}")
    print(f"Message : {decision.get('message', guardian.get('reason'))}")

    event = guardian.get("event")
    if event:
        print(f"Risk    : {event.get('risk')}")
        print(f"Target  : {event.get('target')}")
        print(f"Source  : {event.get('source')}")

    print("=" * 72)


if __name__ == "__main__":
    main()
''',
}


def main():
    print()
    print("=" * 72)
    print("Building Guardian Kernel™")
    print("=" * 72)

    for relative_path, content in FILES.items():
        path = ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"✓ Wrote {relative_path}")

    print("=" * 72)
    print("Guardian Kernel™ files created.")
    print()
    print("Next run:")
    print("python3 -m py_compile aletheus/runtime/guardian/*.py tools/maintenance/run_guardian_kernel.py")
    print()
    print("Then test:")
    print('python3 tools/maintenance/run_guardian_kernel.py --action "delete" --target "vault" --source "guardian-test"')
    print("=" * 72)


if __name__ == "__main__":
    main()
