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
        default=Path("reports/architecture/kinekt/horizontal_mesh_verification"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "mesh_synthesis/mesh-synthesis-graph.json",
        root / "bolt_connectors/bolt-connector-registry.json",
        args.output,
    ).build()
    print(
        f"Horizontal Mesh Verification complete: connected={report['horizontal_mesh_connected']}."
    )
    return 0
