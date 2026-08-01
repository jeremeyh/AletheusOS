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
        default=Path("reports/architecture/kinekt/semantic_throughput"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "wiring/constitutional-wiring-manifest.json",
        root / "data_contracts/constitutional-data-contracts.json",
        root / "structural_hardening/structural-brace-plan.json",
        root / "runtime_telemetry/runtime-telemetry.json",
        args.output,
    ).build()
    print(
        "Semantic Throughput Optimization complete: "
        f"routes={report['route_count']}, batches={report['batch_count']}, "
        f"continuity={report['semantic_continuity_preserved']}."
    )
    return 0
