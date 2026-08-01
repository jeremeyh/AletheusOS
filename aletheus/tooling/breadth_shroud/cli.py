from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/breadth"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        root / "knowledge_graph/runtime-knowledge-graph.json",
        root / "runtime_observability/runtime-observability.json",
        args.output,
    ).build()
    print(
        "Breadth Shroud Layer complete: "
        f"scope={report['awareness_scope']}, readiness={report['readiness']}."
    )
    return 0
