"""Query architectural twin snapshots."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .loader import load_object


def query_node(snapshot_path: Path, node_id: str) -> dict[str, Any] | None:
    snapshot = load_object(snapshot_path)
    for node in snapshot.get("nodes", []):
        if isinstance(node, dict) and node.get("node_id") == node_id:
            return node
    return None
