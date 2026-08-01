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
        default=Path("reports/architecture/kinekt/capability_dependency_graph"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "authority/capability-authority-map.json",
        (root / "engine_registry_realization" / "engine-registry-realization.json"),
        args.output,
    ).build()
    print(
        "Capability Dependency Graph complete: "
        f"capabilities={report['capability_count']}, "
        f"implemented={report['implemented_count']}."
    )
    return 0
