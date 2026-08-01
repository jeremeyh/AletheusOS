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
        default=Path("reports/architecture/kinekt/runtime_diagnostics"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "runtime_observability/runtime-observability.json",
        root / "governance/governance-findings.json",
        args.output,
    ).build()
    print(f"Runtime Diagnostics complete: findings={report['diagnostic_count']}.")
    return 0
