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
        default=Path("reports/architecture/kinekt/pss_core"),
    )
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    metric_module = __import__(
        "aletheus.tooling.pss_core.models",
        fromlist=["Metric"],
    )
    report = Engine().evaluate([metric_module.Metric("quality", 100.0)]).to_dict()
    (args.output / "pss_core.json").write_text(
        json.dumps(report, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("Production Success Standard Core complete.")
    return 0
