from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", nargs="?", default="smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/autonomous_release_intelligence"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = Engine().recommend(
        production_score=100,
        regression_confidence=100,
        compatibility=100,
        rollback_confidence=100,
    )
    (args.output / "autonomous_release_intelligence.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Autonomous Release Intelligence complete.")
    return 0
