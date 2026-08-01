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
        default=Path("reports/architecture/constitutional_ui/nuclear_cloud"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "nuclear_cloud.json").write_text(
        json.dumps(
            {
                "module": "nuclear_cloud",
                "title": "Nuclear Cloud Reason Density",
                "status": "ready",
                "axiomUX": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Nuclear Cloud Reason Density complete.")
    return 0
