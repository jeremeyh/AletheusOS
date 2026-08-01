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
        default=Path("reports/architecture/constitutional_ui/primordial_field"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "primordial_field.json").write_text(
        json.dumps(
            {
                "module": "primordial_field",
                "title": "Primordial Experience Field",
                "status": "ready",
                "axiomUX": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("Primordial Experience Field complete.")
    return 0
