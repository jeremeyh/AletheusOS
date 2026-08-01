from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class WiringEngine:
    def __init__(self, mesh_graph: Path, catalog: Path, output: Path) -> None:
        self.mesh_graph = mesh_graph
        self.catalog = catalog
        self.output = output

    def build(self) -> dict[str, Any]:
        graph = json.loads(self.mesh_graph.read_text(encoding="utf-8"))
        catalog = json.loads(self.catalog.read_text(encoding="utf-8"))
        entries = {
            str(item.get("name")): item
            for item in catalog.get("entries", [])
            if isinstance(item, dict)
        }

        routes: list[dict[str, Any]] = []
        invalid: list[dict[str, str]] = []
        for edge in graph.get("edges", []):
            if not isinstance(edge, dict):
                continue
            source = edge.get("source")
            target = edge.get("target")
            if not isinstance(source, str) or not isinstance(target, str):
                continue
            if source not in entries or target not in entries:
                invalid.append({"source": source, "target": target})
                continue
            routes.append(
                {
                    "route_id": f"{source}::{target}",
                    "source": source,
                    "target": target,
                    "source_category": entries[source].get("category"),
                    "target_category": entries[target].get("category"),
                    "handoff": "evidence_and_request",
                    "status": "declared",
                }
            )

        manifest = {
            "routes": routes,
            "invalid_routes": invalid,
            "route_count": len(routes),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-wiring-manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
        )
        (self.output / "wiring-gaps.json").write_text(
            json.dumps({"invalid_routes": invalid}, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        (self.output / "constitutional-wiring.md").write_text(
            "# Constitutional Wiring\n\n"
            f"- Routes: **{len(routes)}**\n"
            f"- Invalid routes: **{len(invalid)}**\n",
            encoding="utf-8",
        )
        return manifest
