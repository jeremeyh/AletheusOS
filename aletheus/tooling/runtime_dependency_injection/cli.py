from __future__ import annotations

import argparse
from pathlib import Path

from .engine import InjectionEngine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/runtime_dependency_injection"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = InjectionEngine(
        root / "engine_registry_realization/engine-registry-realization.json",
        root / "authority/capability-authority-map.json",
        args.output,
    ).build()
    print(f"Runtime Dependency Injection complete: bindings={report['binding_count']}.")
    return 0
