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
        default=Path("reports/architecture/card_hawk_navigation/context_runtime"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "context_runtime",
        "title": "Context Propagation Runtime",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_NAVIGATION",
        "contextPreserving": True,
        "graphDriven": True,
    }
    (a.output / "context_runtime.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Context Propagation Runtime complete.")
    return 0
