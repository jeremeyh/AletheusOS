from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, wiring: Path, output: Path) -> None:
        self.wiring = wiring
        self.output = output

    def build(self) -> dict[str, Any]:
        wiring = json.loads(self.wiring.read_text(encoding="utf-8"))
        edges = [
            (str(item.get("source")), str(item.get("target")))
            for item in wiring.get("routes", [])
            if isinstance(item, dict)
        ]
        reverse = {(target, source) for source, target in edges}
        cycles = []
        seen = set()
        for source, target in edges:
            pair = tuple(sorted((source, target)))
            if pair in seen or (source, target) not in reverse:
                continue
            seen.add(pair)
            lowered = f"{source} {target}".casefold()
            semantic = (
                "telemetry_feedback"
                if "telemetry" in lowered or "observ" in lowered
                else "governance_feedback"
                if "council" in lowered or "govern" in lowered
                else "learning_feedback"
                if "memory" in lowered or "learning" in lowered
                else "bidirectional_collaboration"
            )
            cycles.append(
                {
                    "members": list(pair),
                    "semantic_class": semantic,
                    "intentional": True,
                }
            )

        report = {
            "cycle_groups": cycles,
            "cycle_group_count": len(cycles),
            "unclassified_cycles": [
                item
                for item in cycles
                if item["semantic_class"] == "bidirectional_collaboration"
            ],
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "cyclic-flow-semantics.json").write_text(
            json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
        )
        return report
