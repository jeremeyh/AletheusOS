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
        default=Path("reports/architecture/kinekt/validator_composition"),
    )
    args = parser.parse_args()
    report = Engine(
        Path(
            "reports/architecture/kinekt/process_grid_consolidation/process-grid-consolidation.json"
        ),
        args.output,
    ).build()
    print(f"Validator Composition complete: validators={report['validator_count']}.")
    return 0
