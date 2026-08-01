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
        default=Path("reports/architecture/kinekt/process_composer"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "process_grid_runtime/process-grid-runtime.json",
        root / "engine_registry_realization/engine-registry-realization.json",
        root / "authority/capability-authority-map.json",
        args.output,
    ).build()
    print(
        "Constitutional Process Composer complete: "
        f"steps={report['step_count']}, "
        f"engines={report['registered_engines']}, "
        f"parallel_gate_layer={report['parallel_gate_layer_created']}."
    )
    return 0
