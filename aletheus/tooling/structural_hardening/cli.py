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
        default=Path("reports/architecture/kinekt/structural_hardening"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "semantic_topology/semantic-root-classification.json",
        root / "cyclic_flow_semantics/cyclic-flow-semantics.json",
        root / "platform_continuity/full-platform-continuity-gate.json",
        args.output,
    ).build()
    print(
        "Structural Hardening complete: "
        f"braces={report['brace_count']}, "
        f"parallel_layer={report['parallel_layer_created']}."
    )
    return 0
