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
        default=Path("reports/architecture/card_hawk/nuclear_cloud"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "nuclear_cloud",
        "title": "Nuclear Cloud Reason Field",
        "status": "ready",
        "application": "CARD_HAWK",
        "voice": "A3YE",
        "unconcealedTruth": True,
    }
    target = args.output / "nuclear_cloud.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Nuclear Cloud Reason Field complete.")
    return 0
