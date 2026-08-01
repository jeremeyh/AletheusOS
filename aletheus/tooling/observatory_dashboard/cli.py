from __future__ import annotations

import argparse
from pathlib import Path

from .engine import DashboardEngine


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="python -m aletheus.tooling.observatory_dashboard"
    )
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/observatory_dashboard"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    dashboard = DashboardEngine(
        {
            "observatory": root / "observatory/platform-observatory.json",
            "mission_control": root / "mission_control/mission-control.json",
            "com": root / "com/cognitive-mesh.json",
            "twin": root / "twin/architectural-digital-twin.json",
        },
        args.output,
    ).build()
    print(
        "Observatory Dashboard complete: "
        f"cards={len(dashboard['cards'])}, "
        f"readiness={dashboard['readiness']}."
    )
    return 0
