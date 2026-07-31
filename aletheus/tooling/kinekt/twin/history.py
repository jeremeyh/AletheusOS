"""Twin history and change comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import load_object


def compare_previous(
    current: dict[str, Any],
    previous_path: Path | None,
) -> dict[str, Any]:
    if previous_path is None or not previous_path.is_file():
        return {"status": "baseline"}

    previous = load_object(previous_path)
    previous_nodes = {
        item["node_id"]
        for item in previous.get("nodes", [])
        if isinstance(item, dict) and "node_id" in item
    }
    current_nodes = {
        item["node_id"]
        for item in current.get("nodes", [])
        if isinstance(item, dict) and "node_id" in item
    }

    return {
        "status": "compared",
        "nodes_added": sorted(current_nodes - previous_nodes),
        "nodes_removed": sorted(previous_nodes - current_nodes),
        "previous_snapshot_id": previous.get("snapshot_id"),
    }
