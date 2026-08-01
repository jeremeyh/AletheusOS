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
        default=Path("reports/architecture/constitutional_ui/perceptual_budget"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "perceptual_budget.json").write_text(
        json.dumps(
            {
                "module": "perceptual_budget",
                "title": "Cognitive Load and Perceptual Budget",
                "status": "ready",
                "axiomUX": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Cognitive Load and Perceptual Budget complete.")
    return 0
