from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_compatibility"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        (root / "engine_registry_realization" / "engine-registry-realization.json"),
        root / "process_composer/constitutional-process-composition.json",
        args.output,
    ).build()
    print(
        "Runtime Compatibility complete: " f"compatible={report['compatible_count']}."
    )
    return 0 if report["incompatible_count"] == 0 else 1
