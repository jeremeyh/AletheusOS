from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, wiring: Path, contracts: Path, output: Path) -> None:
        self.wiring = wiring
        self.contracts = contracts
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        contracts = json.loads(self.contracts.read_text(encoding="utf-8"))
        channels = {
            item.get("channel_id")
            for item in contracts.get("contracts", [])
            if isinstance(item, dict)
        }
        rails = []
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            channel_id = f"bus::{route.get('source')}::{route.get('target')}"
            rails.append(
                {
                    "rail_id": f"out::{channel_id}",
                    "direction": "outbound",
                    "source": route.get("source"),
                    "target": route.get("target"),
                    "contract_present": channel_id in channels,
                    "state": "open_bounded",
                }
            )
        report = {"outbound_rails": rails, "rail_count": len(rails)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "outbound-rail-state.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
