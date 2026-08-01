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
        default=Path("reports/architecture/kinekt/outbound_rails"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "wiring/constitutional-wiring-manifest.json",
        root / "data_contracts/constitutional-data-contracts.json",
        args.output,
    ).build()
    print(f"Outbound Rail State complete: rails={report['rail_count']}.")
    return 0
