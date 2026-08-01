from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="smoke")
    parser.add_argument(
        "--output", type=Path, default=Path("reports/architecture/nimble/visualization")
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "visualization",
        "title": "Visualization Primitives",
        "status": "ready",
        "engine": type(Engine()).__name__,
    }
    (args.output / "visualization.json").write_text(
        json.dumps(report, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Visualization Primitives complete.")
    return 0
