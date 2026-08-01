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
        default=Path("reports/architecture/card_hawk/thorx_bridge"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "thorx_bridge",
        "title": "THORᵡ Card Decision Bridge",
        "status": "ready",
        "application": "CARD_HAWK",
        "voice": "A3YE",
        "unconcealedTruth": True,
    }
    target = args.output / "thorx_bridge.json"
    target.write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("THORᵡ Card Decision Bridge complete.")
    return 0
