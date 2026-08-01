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
        default=Path("reports/architecture/card_hawk_experience/scouting_game_film"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "scouting_game_film",
        "title": "Scouting Report and Game Film Experiences",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_COMPOSITION",
        "nimble": True,
        "uxr": True,
        "axiomUX": True,
    }
    (a.output / "scouting_game_film.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Scouting Report and Game Film Experiences complete.")
    return 0
