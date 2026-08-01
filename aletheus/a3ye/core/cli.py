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
        default=Path("reports/architecture/a3ye/core"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {
        "module": "core",
        "title": "A•3ye Core",
        "status": "ready",
        "runtime": "A3YE",
        "constitutionalVoice": True,
        "unconcealedTruth": True,
    }
    (args.output / "core.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("A•3ye Core complete.")
    return 0
