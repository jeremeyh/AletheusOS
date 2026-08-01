from __future__ import annotations

import json
from pathlib import Path
from typing import Any

CORE_SEQUENCE = [
    "Evidence Engine",
    "Knowledge Engine",
    "Reason Engine",
    "Memory Engine",
    "Predictive Engine",
    "Planning Engine",
    "Decision Engine",
]


class Engine:
    def __init__(self, registry: Path, output: Path) -> None:
        self.registry = registry
        self.output = output

    def build(self) -> dict[str, Any]:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        engines = {
            item.get("engine_name"): item
            for item in registry.get("engines", [])
            if isinstance(item, dict)
        }
        participants = [
            {
                "engine": name,
                "registered": name in engines,
                "mesh_role": "intelligence_participant",
            }
            for name in CORE_SEQUENCE
        ]
        routes = [
            {"source": CORE_SEQUENCE[i], "target": CORE_SEQUENCE[i + 1]}
            for i in range(len(CORE_SEQUENCE) - 1)
        ]
        report = {
            "participants": participants,
            "routes": routes,
            "coordination_mode": "live_runtime_coordination",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "intelligence-mesh-runtime.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
