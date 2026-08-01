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
        default=Path("reports/architecture/card_hawk/core"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "core",
        "title": "Card Hawk Intelligence Core",
        "status": "ready",
        "application": "CARD_HAWK",
        "voice": "A3YE",
        "unconcealedTruth": True,
    }
    target = args.output / "core.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Card Hawk Intelligence Core complete.")
    return 0
