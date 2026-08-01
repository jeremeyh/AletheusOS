from __future__ import annotations

import argparse
from pathlib import Path

from .engine import ObservatoryEngine


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.observatory")
    parser.add_argument("command", choices=("analyze",), nargs="?", default="analyze")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/observatory"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = ObservatoryEngine(
        root / "health/constitutional-health.json",
        root / "authority/capability-authority-map.json",
        root / "twin/architectural-digital-twin.json",
        root / "orchestration/execution-manifest.json",
        args.output,
    ).analyze()
    print(
        "Aletheus Observatory complete: "
        f"health={report.health_score:.2f}, "
        f"coverage={report.authority_coverage:.2f}%, "
        f"alerts={len(report.alerts)}."
    )
    return 0
