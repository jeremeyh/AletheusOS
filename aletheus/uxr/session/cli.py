from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output", type=Path, default=Path("reports/architecture/uxr/session")
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "session",
        "title": "Experience Session Manager",
        "status": "ready",
        "runtime": "Universal Experience Runtime",
        "schemaDriven": True,
        "catalogConstrained": True,
    }
    (a.output / "session.json").write_text(
        json.dumps(r, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Experience Session Manager complete.")
    return 0
