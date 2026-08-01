from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("plan",), nargs="?", default="plan")
    parser.add_argument("--environment", default="production")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/unified_production_installer"),
    )
    args = parser.parse_args()
    report = Engine(args.output).plan(args.environment)
    print("Unified Production Installer complete: " f"stages={report['stage_count']}.")
    return 0
