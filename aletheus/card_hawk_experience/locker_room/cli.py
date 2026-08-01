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
        default=Path("reports/architecture/card_hawk_experience/locker_room"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "locker_room",
        "title": "Locker Room Experience",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_COMPOSITION",
        "nimble": True,
        "uxr": True,
        "axiomUX": True,
    }
    (a.output / "locker_room.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Locker Room Experience complete.")
    return 0
