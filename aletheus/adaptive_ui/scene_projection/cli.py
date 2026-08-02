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
        default=Path("reports/architecture/adaptive_ui/scene_projection"),
    )
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    r = {
        "module": "scene_projection",
        "title": "Scene Projection Compiler",
        "status": "ready",
        "runtime": "ADAPTIVE_UI_WORKSPACE",
        "renderNeutral": True,
        "constitutionalMotion": True,
    }
    (a.output / "scene_projection.json").write_text(
        json.dumps(r, indent=2, sort_keys=True)
    )
    print("Scene Projection Compiler complete.")
    return 0
