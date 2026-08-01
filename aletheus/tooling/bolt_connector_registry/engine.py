from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, registry: Path, wiring: Path, output: Path) -> None:
        self.registry = registry
        self.wiring = wiring
        self.output = output

    def build(self) -> dict[str, Any]:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        engines = {
            item.get("engine_name"): item
            for item in registry.get("engines", [])
            if isinstance(item, dict)
        }

        connectors = []
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            source = str(route.get("source"))
            target = str(route.get("target"))
            connectors.append(
                {
                    "connector_id": f"bolt::{source}::{target}",
                    "source": source,
                    "target": target,
                    "source_registered": source in engines,
                    "target_registered": target in engines,
                    "connector_type": "constitutional_bolt",
                    "status": "declared",
                }
            )

        report = {"connectors": connectors, "connector_count": len(connectors)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "bolt-connector-registry.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
