from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, inbound: Path, outbound: Path, output: Path) -> None:
        self.inbound = inbound
        self.outbound = outbound
        self.output = output

    def build(self) -> dict[str, Any]:
        inbound = json.loads(self.inbound.read_text(encoding="utf-8"))
        outbound = json.loads(self.outbound.read_text(encoding="utf-8"))
        in_count = inbound.get("rail_count", 0)
        out_count = outbound.get("rail_count", 0)
        report = {
            "inbound_rails": in_count,
            "outbound_rails": out_count,
            "paired_rails": min(in_count, out_count),
            "parallel_in_out_enabled": in_count == out_count and in_count > 0,
            "flow_state": "full_duplex_bounded",
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "parallel-rail-coordination.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
