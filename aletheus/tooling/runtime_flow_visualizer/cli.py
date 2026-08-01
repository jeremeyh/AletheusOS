from __future__ import annotations

import argparse
from pathlib import Path

from .engine import FlowVisualizerEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_flows"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = FlowVisualizerEngine(
        root / "wiring/constitutional-wiring-manifest.json",
        root / "data_contracts/constitutional-data-contracts.json",
        args.output,
    ).build()
    print(f"Runtime Flow Visualizer complete: flows={report['flow_count']}.")
    return 0
