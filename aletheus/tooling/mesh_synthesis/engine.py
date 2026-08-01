from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def normalize(name: str) -> str:
    return "".join(ch for ch in name.casefold() if ch.isalnum())


class MeshSynthesisEngine:
    def __init__(self, catalog: Path, output: Path) -> None:
        self.catalog = catalog
        self.output = output

    def build(self) -> dict[str, Any]:
        payload = json.loads(self.catalog.read_text(encoding="utf-8"))
        entries = payload.get("entries", [])
        if not isinstance(entries, list):
            raise TypeError("Catalog entries must be a list.")

        names = {
            normalize(str(item.get("name", ""))): str(item.get("name", ""))
            for item in entries
            if isinstance(item, dict)
        }
        edges: list[dict[str, str]] = []
        missing_targets: list[dict[str, str]] = []
        incoming: dict[str, int] = defaultdict(int)
        outgoing: dict[str, int] = defaultdict(int)

        for item in entries:
            if not isinstance(item, dict):
                continue
            source = str(item.get("name", ""))
            for target in item.get("mesh_connections", []):
                target_name = str(target)
                target_key = normalize(target_name)
                if target_key not in names:
                    missing_targets.append({"source": source, "target": target_name})
                    continue
                canonical_target = names[target_key]
                edges.append({"source": source, "target": canonical_target})
                outgoing[source] += 1
                incoming[canonical_target] += 1

        disconnected = sorted(
            str(item.get("name", ""))
            for item in entries
            if isinstance(item, dict)
            and incoming[str(item.get("name", ""))] == 0
            and outgoing[str(item.get("name", ""))] == 0
        )

        graph = {
            "nodes": [
                str(item.get("name", "")) for item in entries if isinstance(item, dict)
            ],
            "edges": edges,
            "disconnected": disconnected,
            "missing_targets": missing_targets,
        }

        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "mesh-synthesis-graph.json").write_text(
            json.dumps(graph, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.output / "mesh-realization-gaps.json").write_text(
            json.dumps(
                {
                    "disconnected": disconnected,
                    "missing_targets": missing_targets,
                },
                indent=2,
                sort_keys=True,
            ),
            encoding="utf-8",
        )
        (self.output / "mesh-synthesis.md").write_text(
            "# Mesh Synthesis\n\n"
            f"- Nodes: **{len(graph['nodes'])}**\n"
            f"- Edges: **{len(edges)}**\n"
            f"- Disconnected: **{len(disconnected)}**\n"
            f"- Missing targets: **{len(missing_targets)}**\n",
            encoding="utf-8",
        )
        return graph
