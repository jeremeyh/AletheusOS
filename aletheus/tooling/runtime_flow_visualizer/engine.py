from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def safe_id(value: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in value)


class FlowVisualizerEngine:
    def __init__(self, wiring: Path, contracts: Path, output: Path) -> None:
        self.wiring = wiring
        self.contracts = contracts
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        contracts = json.loads(self.contracts.read_text(encoding="utf-8"))
        contract_channels = {
            item.get("channel_id")
            for item in contracts.get("contracts", [])
            if isinstance(item, dict)
        }

        flows: list[dict[str, Any]] = []
        mermaid = ["flowchart LR"]
        for route in wiring.get("routes", []):
            if not isinstance(route, dict):
                continue
            source = str(route.get("source"))
            target = str(route.get("target"))
            channel_id = f"bus::{source}::{target}"
            flows.append(
                {
                    "source": source,
                    "target": target,
                    "channel_id": channel_id,
                    "contract_present": channel_id in contract_channels,
                }
            )
            mermaid.append(
                f"    {safe_id(source)}[{source}] --> {safe_id(target)}[{target}]"
            )

        report = {"flows": flows, "flow_count": len(flows)}
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-flows.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "runtime-flows.mmd").write_text(
            "\n".join(mermaid),
            encoding="utf-8",
        )
        (self.output / "runtime-flow-summary.md").write_text(
            "# Runtime Flow Visualizer\n\n"
            f"- Flows: **{len(flows)}**\n"
            f"- Contracted: **{sum(item['contract_present'] for item in flows)}**\n",
            encoding="utf-8",
        )
        return report
