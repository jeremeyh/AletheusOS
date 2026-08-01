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
        default=Path("reports/architecture/card_hawk_experience/overlay_runtime"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "overlay_runtime",
        "title": "Universal Intelligence Overlay Runtime",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_COMPOSITION",
        "nimble": True,
        "uxr": True,
        "axiomUX": True,
    }
    (a.output / "overlay_runtime.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Universal Intelligence Overlay Runtime complete.")
    return 0
