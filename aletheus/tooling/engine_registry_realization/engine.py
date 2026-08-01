from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, catalog: Path, contracts: Path, bus: Path, output: Path) -> None:
        self.catalog = catalog
        self.contracts = contracts
        self.bus = bus
        self.output = output

    def build(self) -> dict[str, Any]:
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        contracts = json.loads(self.contracts.read_text(encoding="utf-8"))
        bus = json.loads(self.bus.read_text(encoding="utf-8"))
        contract_channels = {
            item.get("channel_id")
            for item in contracts.get("contracts", [])
            if isinstance(item, dict)
        }
        bus_channels = {
            item.get("channel_id")
            for item in bus.get("channels", [])
            if isinstance(item, dict)
        }

        engines = []
        for item in catalog.get("entries", []):
            if not isinstance(item, dict):
                continue
            category = str(item.get("category", ""))
            if "engine" not in str(
                item.get("name", "")
            ).casefold() and category not in {
                "core_intelligence",
                "platform_runtime",
                "security_intelligence",
                "perception",
            }:
                continue
            name = str(item.get("name", ""))
            expected_channels = {
                f"bus::{name}::{target}" for target in item.get("mesh_connections", [])
            }
            engines.append(
                {
                    "engine_name": name,
                    "authority": item.get("authority"),
                    "lifecycle": "registered",
                    "runtime_authority": item.get("parent"),
                    "service_bus_channels": sorted(expected_channels & bus_channels),
                    "contract_channels": sorted(expected_channels & contract_channels),
                    "status": "realized",
                }
            )

        report = {"engines": engines, "engine_count": len(engines)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "engine-registry-realization.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
