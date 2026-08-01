from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class Engine:
    def __init__(self, authority: Path, registry: Path, output: Path) -> None:
        self.authority = authority
        self.registry = registry
        self.output = output

    def build(self) -> dict[str, Any]:
        authority = json.loads(self.authority.read_text(encoding="utf-8"))
        registry = json.loads(self.registry.read_text(encoding="utf-8"))
        capabilities = [
            item for item in authority.get("capabilities", []) if isinstance(item, dict)
        ]
        engines = {
            str(item.get("engine_name"))
            for item in registry.get("engines", [])
            if isinstance(item, dict)
        }
        nodes = []
        edges = []
        for item in capabilities:
            name = str(item.get("name"))
            nodes.append(
                {
                    "capability": name,
                    "authority": item.get("authority"),
                    "implemented": name in engines,
                }
            )
            parent = item.get("parent")
            if parent:
                edges.append(
                    {
                        "source": str(parent),
                        "target": name,
                        "kind": "contains",
                    }
                )
        report = {
            "nodes": nodes,
            "edges": edges,
            "capability_count": len(nodes),
            "implemented_count": sum(1 for item in nodes if item["implemented"]),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "capability-dependency-graph.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
