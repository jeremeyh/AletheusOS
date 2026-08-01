from __future__ import annotations

import argparse
from pathlib import Path

from .engine import WiringEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("build", "validate"), nargs="?", default="build"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/wiring"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = WiringEngine(
        root / "mesh_synthesis/mesh-synthesis-graph.json",
        root / "ecosystem_catalog/canonical-ecosystem-catalog.json",
        args.output,
    ).build()
    print(
        "Constitutional Wiring complete: "
        f"routes={report['route_count']}, "
        f"invalid={len(report['invalid_routes'])}."
    )
    if args.command == "validate" and report["invalid_routes"]:
        return 1
    return 0
