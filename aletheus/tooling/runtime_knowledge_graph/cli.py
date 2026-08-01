from __future__ import annotations

import argparse
from pathlib import Path

from .engine import KnowledgeGraphEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/knowledge_graph"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    graph = KnowledgeGraphEngine(
        root / "registry/constitutional-registry.json",
        root / "twin/architectural-digital-twin.json",
        args.output,
    ).build()
    print(
        "Runtime Knowledge Graph complete: "
        f"nodes={len(graph['nodes'])}, "
        f"relationships={len(graph['relationships'])}."
    )
    return 0
