from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output", type=Path, default=Path("reports/architecture/kinekt/path_resolver")
    )
    args = parser.parse_args()
    report = Engine(
        Path("reports/architecture/kinekt/wiring/constitutional-wiring-manifest.json"),
        args.output,
    ).build()
    print(
        f"End-to-End Path Resolver complete: nodes={len(report['nodes'])}, roots={len(report['roots'])}, leaves={len(report['leaves'])}."
    )
    return 0
