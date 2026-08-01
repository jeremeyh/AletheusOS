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
        default=Path("reports/architecture/card_hawk/experience_projection"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "experience_projection",
        "title": "Collector Experience Projection",
        "status": "ready",
        "application": "CARD_HAWK",
        "voice": "A3YE",
        "unconcealedTruth": True,
    }
    target = args.output / "experience_projection.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Collector Experience Projection complete.")
    return 0
