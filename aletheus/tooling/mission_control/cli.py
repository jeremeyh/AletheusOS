from __future__ import annotations

import argparse
from pathlib import Path

from .engine import MissionControlEngine


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.mission_control")
    parser.add_argument("command", choices=("plan",), nargs="?", default="plan")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/mission_control"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = MissionControlEngine(
        root / "observatory/platform-observatory.json",
        root / "orchestration/execution-manifest.json",
        args.output,
    ).plan()
    print(
        "Aletheus Mission Control complete: "
        f"missions={len(report.missions)}, readiness={report.readiness}."
    )
    return 0
