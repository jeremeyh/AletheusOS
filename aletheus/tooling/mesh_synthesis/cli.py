from __future__ import annotations

import argparse
from pathlib import Path

from .engine import MeshSynthesisEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", choices=("build", "validate"), nargs="?", default="build"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/mesh_synthesis"),
    )
    args = parser.parse_args()
    report = MeshSynthesisEngine(
        Path(
            "reports/architecture/kinekt/ecosystem_catalog/canonical-ecosystem-catalog.json"
        ),
        args.output,
    ).build()
    print(
        "Mesh Synthesis complete: "
        f"nodes={len(report['nodes'])}, "
        f"edges={len(report['edges'])}, "
        f"disconnected={len(report['disconnected'])}, "
        f"missing_targets={len(report['missing_targets'])}."
    )
    if args.command == "validate" and report["disconnected"]:
        return 1
    return 0
