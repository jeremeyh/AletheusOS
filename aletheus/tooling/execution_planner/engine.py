from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, flows: Path, output: Path) -> None:
        self.flows = flows
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.flows.read_text(encoding="utf-8"))
        flows = payload.get("flows", [])
        if not isinstance(flows, list):
            raise TypeError("Runtime flows must be a list.")

        steps = [
            {
                "step_id": f"step-{index:04d}",
                "source": flow.get("source"),
                "target": flow.get("target"),
                "channel_id": flow.get("channel_id"),
                "contract_present": bool(flow.get("contract_present")),
                "approval_required": True,
            }
            for index, flow in enumerate(flows, start=1)
            if isinstance(flow, dict)
        ]
        plan = {"steps": steps, "step_count": len(steps), "status": "planned"}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-execution-plan.json").write_text(
            json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "execution-plan.md").write_text(
            "# Constitutional Execution Plan\n\n"
            f"- Steps: **{len(steps)}**\n"
            "- Status: **planned**\n",
            encoding="utf-8",
        )
        return plan
