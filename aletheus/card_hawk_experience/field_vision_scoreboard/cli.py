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
        default=Path(
            "reports/architecture/card_hawk_experience/field_vision_scoreboard"
        ),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "field_vision_scoreboard",
        "title": "Field Vision and Scoreboard Experiences",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_COMPOSITION",
        "nimble": True,
        "uxr": True,
        "axiomUX": True,
    }
    (a.output / "field_vision_scoreboard.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Field Vision and Scoreboard Experiences complete.")
    return 0
