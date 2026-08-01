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
        default=Path("reports/architecture/kinekt/parallel_rails"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "inbound_rails/inbound-rail-state.json",
        root / "outbound_rails/outbound-rail-state.json",
        args.output,
    ).build()
    print(
        f"Parallel Rail Coordination complete: enabled={report['parallel_in_out_enabled']}, paired={report['paired_rails']}."
    )
    return 0
