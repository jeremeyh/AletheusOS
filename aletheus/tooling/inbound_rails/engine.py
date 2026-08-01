from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, wiring: Path, access: Path, output: Path) -> None:
        self.wiring = wiring
        self.access = access
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        access = json.loads(self.access.read_text(encoding="utf-8"))
        modules = {
            item.get("channel_id"): item
            for item in access.get("access_modules", [])
            if isinstance(item, dict)
        }
        rails = []
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            channel_id = f"bus::{route.get('source')}::{route.get('target')}"
            rails.append(
                {
                    "rail_id": f"in::{channel_id}",
                    "direction": "inbound",
                    "source": route.get("source"),
                    "target": route.get("target"),
                    "access_module_present": channel_id in modules,
                    "state": "open_bounded",
                }
            )
        report = {"inbound_rails": rails, "rail_count": len(rails)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "inbound-rail-state.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
