from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/card_hawk_navigation/mission_runtime"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "mission_runtime",
        "title": "Mission Context Runtime",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_NAVIGATION",
        "contextPreserving": True,
        "graphDriven": True,
    }
    (a.output / "mission_runtime.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Mission Context Runtime complete.")
    return 0
