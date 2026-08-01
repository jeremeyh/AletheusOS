from __future__ import annotations

import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = [
    "authority",
    "message_type",
    "evidence_refs",
    "provenance",
    "confidence",
    "correlation_id",
    "version",
    "timestamp",
    "policy_context",
]


class DataContractEngine:
    def __init__(self, service_bus: Path, output: Path) -> None:
        self.service_bus = service_bus
        self.output = output

    def build(self) -> dict[str, Any]:
        bus = json.loads(self.service_bus.read_text(encoding="utf-8"))
        contracts = []
        for channel in bus.get("channels", []):
            if not isinstance(channel, dict):
                continue
            contracts.append(
                {
                    "channel_id": channel.get("channel_id"),
                    "schema_version": "1.0",
                    "required_fields": REQUIRED_FIELDS,
                    "confidence_range": [0.0, 1.0],
                    "provenance_required": True,
                    "evidence_required": True,
                }
            )

        report = {
            "contracts": contracts,
            "contract_count": len(contracts),
            "required_fields": REQUIRED_FIELDS,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-data-contracts.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "contract-index.json").write_text(
            json.dumps(
                {item["channel_id"]: item for item in contracts},
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        return report
