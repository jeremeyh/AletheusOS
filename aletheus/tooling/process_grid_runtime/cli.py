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
        default=Path("reports/architecture/kinekt/process_grid_runtime"),
    )
    args = parser.parse_args()
    report = Engine(
        Path(
            "reports/architecture/kinekt/validator_composition/validator-composition.json"
        ),
        args.output,
    ).build()
    print(
        "Process Grid Runtime complete: "
        f"steps={report['step_count']}, state={report['runtime_state']}."
    )
    return 0
