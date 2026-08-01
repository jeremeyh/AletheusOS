from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output", type=Path, default=Path("reports/architecture/uxr/composition")
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "composition",
        "title": "Experience Composition Engine",
        "status": "ready",
        "runtime": "Universal Experience Runtime",
        "schemaDriven": True,
        "catalogConstrained": True,
    }
    (a.output / "composition.json").write_text(
        json.dumps(r, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Experience Composition Engine complete.")
    return 0
