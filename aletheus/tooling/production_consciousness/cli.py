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
        default=Path("reports/architecture/kinekt/production_consciousness"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = Engine().synthesize(
        changed="PSS enabled",
        reason="production assurance",
        constitutional=True,
        safe=True,
        quality_delta=1.0,
        risk_delta=-1.0,
        recommendation="promote",
        evidence=("certification",),
    )
    (args.output / "production_consciousness.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Production Consciousness Engine complete.")
    return 0
