from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, connectors: Path, contracts: Path, output: Path) -> None:
        self.connectors = connectors
        self.contracts = contracts
        self.output = output

    def build(self) -> dict[str, Any]:
        connectors = json.loads(self.connectors.read_text(encoding="utf-8"))
        contracts = json.loads(self.contracts.read_text(encoding="utf-8"))
        contract_channels = {
            item.get("channel_id")
            for item in contracts.get("contracts", [])
            if isinstance(item, dict)
        }

        modules = []
        for connector in connectors.get("connectors", []):
            if not isinstance(connector, dict):
                continue
            source = connector.get("source")
            target = connector.get("target")
            channel_id = f"bus::{source}::{target}"
            modules.append(
                {
                    "access_module_id": f"access::{source}::{target}",
                    "connector_id": connector.get("connector_id"),
                    "channel_id": channel_id,
                    "contract_present": channel_id in contract_channels,
                    "authorization_required": True,
                    "authentication_required": True,
                }
            )
        report = {"access_modules": modules, "access_module_count": len(modules)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "access-module-realization.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
