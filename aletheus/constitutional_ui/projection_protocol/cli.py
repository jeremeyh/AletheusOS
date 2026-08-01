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
        default=Path("reports/architecture/constitutional_ui/projection_protocol"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    (a.output / "projection_protocol.json").write_text(
        json.dumps(
            {
                "module": "projection_protocol",
                "title": "AxiomUX Projection Protocol",
                "status": "ready",
                "axiomUX": True,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("AxiomUX Projection Protocol complete.")
    return 0
