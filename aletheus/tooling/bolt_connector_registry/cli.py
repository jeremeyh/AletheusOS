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
        default=Path("reports/architecture/kinekt/bolt_connectors"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "engine_registry_realization/engine-registry-realization.json",
        root / "wiring/constitutional-wiring-manifest.json",
        args.output,
    ).build()
    print(f"Bolt Connector Registry complete: connectors={report['connector_count']}.")
    return 0
