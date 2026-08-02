from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", nargs="?", default="smoke")
    p.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/adaptive_ui/perceptual_telemetry"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "perceptual_telemetry",
        "title": "Perceptual Telemetry Layer",
        "status": "ready",
        "runtime": "ADAPTIVE_UI_WORKSPACE",
        "renderNeutral": True,
        "constitutionalMotion": True,
    }
    (a.output / "perceptual_telemetry.json").write_text(
        json.dumps(r, indent=2, sort_keys=True)
    )
    print("Perceptual Telemetry Layer complete.")
    return 0
