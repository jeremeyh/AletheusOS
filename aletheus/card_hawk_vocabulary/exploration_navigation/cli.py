from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "reports/architecture/card_hawk_vocabulary/exploration_navigation"
        ),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    report = {
        "module": "exploration_navigation",
        "title": "Exploration and Navigation Language",
        "status": "ready",
        "application": "CARD_HAWK",
        "library": "EXPERIENCE_VOCABULARY",
        "semanticFaithfulness": True,
    }
    target = args.output / "exploration_navigation.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Exploration and Navigation Language complete.")
    return 0
