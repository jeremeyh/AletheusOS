from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROCESS_ORDER = [
    "Identity Validation",
    "Authority Resolution",
    "Evidence Validation",
    "Knowledge Resolution",
    "Semantic Validation",
    "Planning",
    "Decision",
    "Mission Authorization",
    "Runtime Orchestration",
    "Service Bus Routing",
    "Execution",
    "Telemetry",
    "Runtime Health",
    "Mesh Validation",
    "Architecture Validation",
    "Governance Validation",
    "Platform Certification",
]


class Engine:
    def __init__(self, validators: Path, output: Path) -> None:
        self.validators = validators
        self.output = output

    def build(self) -> dict[str, Any]:
        validators = json.loads(self.validators.read_text(encoding="utf-8"))
        by_stage = {
            item.get("stage"): item
            for item in validators.get("validators", [])
            if isinstance(item, dict)
        }
        steps = []
        for index, stage in enumerate(PROCESS_ORDER, start=1):
            validator = by_stage.get(stage)
            steps.append(
                {
                    "step_id": f"process-{index:02d}",
                    "stage": stage,
                    "validator_id": validator.get("validator_id")
                    if validator
                    else None,
                    "status": "ready",
                    "execution_mode": "ordered",
                }
            )
        report = {
            "generated_at": datetime.now(UTC).isoformat(),
            "steps": steps,
            "step_count": len(steps),
            "runtime_state": "assembled",
            "single_final_verdict_stage": "Platform Certification",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "process-grid-runtime.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
