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
        default=Path("reports/architecture/card_hawk_navigation/experience_mesh"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "experience_mesh",
        "title": "Experience Mesh",
        "status": "ready",
        "application": "CARD_HAWK",
        "runtime": "EXPERIENCE_NAVIGATION",
        "contextPreserving": True,
        "graphDriven": True,
    }
    (a.output / "experience_mesh.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Experience Mesh complete.")
    return 0
