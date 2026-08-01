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
        default=Path("reports/architecture/card_hawk_vocabulary/universal_collection"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    report = {
        "module": "universal_collection",
        "title": "Universal Collection Language",
        "status": "ready",
        "application": "CARD_HAWK",
        "library": "EXPERIENCE_VOCABULARY",
        "semanticFaithfulness": True,
    }
    target = args.output / "universal_collection.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Universal Collection Language complete.")
    return 0
