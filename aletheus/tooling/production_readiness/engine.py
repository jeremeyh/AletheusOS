from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, health: Path, compatibility: Path, output: Path) -> None:
        self.health = health
        self.compatibility = compatibility
        self.output = output

    def certify(self) -> dict[str, Any]:
        health = json.loads(self.health.read_text(encoding="utf-8"))
        compatibility = json.loads(self.compatibility.read_text(encoding="utf-8"))
        blockers = []
        if not health.get("healthy"):
            blockers.append("Post-install mission health failed.")
        if compatibility.get("incompatible_count", 0):
            blockers.append("Runtime compatibility failures detected.")
        status = "READY" if not blockers else "BLOCKED"
        report = {"status": status, "blockers": blockers}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "production-readiness-certification.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
