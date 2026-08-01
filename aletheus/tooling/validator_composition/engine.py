from __future__ import annotations

import json
from pathlib import Path
from typing import Any

STAGE_ORDER = [
    "Telemetry",
    "Runtime Health",
    "Semantic Validation",
    "Mesh Validation",
    "Architecture Validation",
    "Governance Validation",
    "Platform Certification",
]


class Engine:
    def __init__(self, consolidation: Path, output: Path) -> None:
        self.consolidation = consolidation
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.consolidation.read_text(encoding="utf-8"))
        stages = payload.get("stages", {})
        validators = []
        for index, stage_name in enumerate(STAGE_ORDER, start=1):
            components = stages.get(stage_name, [])
            validators.append(
                {
                    "validator_id": f"validator-{index:02d}",
                    "stage": stage_name,
                    "interface": "validate(context) -> ValidationResult",
                    "components": [
                        item.get("absorbed_component")
                        for item in components
                        if isinstance(item, dict)
                    ],
                    "enabled": True,
                }
            )
        report = {
            "validators": validators,
            "validator_count": len(validators),
            "common_interface": "validate(context) -> ValidationResult",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "validator-composition.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
