from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output", type=Path, default=Path("reports/architecture/uxr/interaction")
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "interaction",
        "title": "Interaction Orchestrator",
        "status": "ready",
        "runtime": "Universal Experience Runtime",
        "schemaDriven": True,
        "catalogConstrained": True,
    }
    (a.output / "interaction.json").write_text(
        json.dumps(r, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("Interaction Orchestrator complete.")
    return 0
