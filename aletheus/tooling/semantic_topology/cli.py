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
        default=Path("reports/architecture/kinekt/semantic_topology"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "path_resolver/end-to-end-path-resolver.json",
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        args.output,
    ).build()
    print(
        "Semantic Topology complete: "
        f"roots={report['root_count']}, ambiguous={len(report['ambiguous_roots'])}."
    )
    return 0
