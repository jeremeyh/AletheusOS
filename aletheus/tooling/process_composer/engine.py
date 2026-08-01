from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(
        self,
        process_grid: Path,
        engine_registry: Path,
        authority_map: Path,
        output: Path,
    ) -> None:
        self.process_grid = process_grid
        self.engine_registry = engine_registry
        self.authority_map = authority_map
        self.output = output

    def build(self) -> dict[str, Any]:
        grid = json.loads(self.process_grid.read_text(encoding="utf-8"))
        registry = json.loads(self.engine_registry.read_text(encoding="utf-8"))
        authority = json.loads(self.authority_map.read_text(encoding="utf-8"))

        engines = [
            item.get("engine_name")
            for item in registry.get("engines", [])
            if isinstance(item, dict)
        ]
        capabilities = [
            item.get("name")
            for item in authority.get("capabilities", [])
            if isinstance(item, dict)
        ]

        composed_steps = []
        for step in grid.get("steps", []):
            if not isinstance(step, dict):
                continue
            composed_steps.append(
                {
                    **step,
                    "engine_registry_bound": bool(engines),
                    "authority_map_bound": bool(capabilities),
                    "composition_source": "registry_plus_authority_map",
                }
            )

        report = {
            "steps": composed_steps,
            "step_count": len(composed_steps),
            "registered_engines": len(engines),
            "authority_capabilities": len(capabilities),
            "composition_mode": "dynamic_bounded",
            "parallel_gate_layer_created": False,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-process-composition.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
