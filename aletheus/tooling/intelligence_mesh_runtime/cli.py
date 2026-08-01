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
        default=Path("reports/architecture/kinekt/intelligence_mesh_runtime"),
    )
    args = parser.parse_args()
    report = Engine(
        Path(
            "reports/architecture/kinekt/engine_registry_realization/engine-registry-realization.json"
        ),
        args.output,
    ).build()
    print(
        "Intelligence Mesh Runtime complete: "
        f"participants={len(report['participants'])}, routes={len(report['routes'])}."
    )
    return 0
