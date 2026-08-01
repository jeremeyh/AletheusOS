from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, plan: Path, output: Path) -> None:
        self.plan = plan
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.plan.read_text(encoding="utf-8"))
        steps = payload.get("steps", [])
        if not isinstance(steps, list):
            raise TypeError("Execution steps must be a list.")

        units = [
            {
                "unit_id": f"unit::{step.get('step_id')}",
                "step_id": step.get("step_id"),
                "status": "awaiting_approval",
                "runtime_binding": "crk_event_bus",
                "rollback_required": True,
            }
            for step in steps
            if isinstance(step, dict)
        ]
        report = {"units": units, "unit_count": len(units)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-orchestration.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
