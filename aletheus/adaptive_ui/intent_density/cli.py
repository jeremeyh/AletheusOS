from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/adaptive_ui/intent_density"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "intent_density",
        "title": "Intent and Density Resolver",
        "status": "ready",
        "runtime": "ADAPTIVE_UI_WORKSPACE",
        "renderNeutral": True,
        "constitutionalMotion": True,
    }
    (a.output / "intent_density.json").write_text(
        json.dumps(r, indent=2, sort_keys=True)
    )
    print("Intent and Density Resolver complete.")
    return 0
