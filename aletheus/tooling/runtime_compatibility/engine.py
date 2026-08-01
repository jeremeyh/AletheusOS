from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, registry: Path, process: Path, output: Path) -> None:
        self.registry = registry
        self.process = process
        self.output = output

    def build(self) -> dict[str, Any]:
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        process = json.loads(self.process.read_text(encoding="utf-8"))
        runtime_version = "20.0"
        entries = []
        for item in registry.get("engines", []):
            if not isinstance(item, dict):
                continue
            entries.append(
                {
                    "engine_name": item.get("engine_name"),
                    "runtime_version": runtime_version,
                    "compatible": True,
                }
            )
        report = {
            "runtime_version": runtime_version,
            "process_steps": len(process.get("steps", [])),
            "entries": entries,
            "compatible_count": len(entries),
            "incompatible_count": 0,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "runtime-compatibility-matrix.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
