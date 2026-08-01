from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build",), nargs="?", default="build")
    parser.add_argument("--manifests-root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/release_graph"),
    )
    args = parser.parse_args()
    report = Engine(args.manifests_root, args.output).build()
    print(
        "Release Graph complete: "
        f"releases={report['release_count']}, "
        f"cycle_free={report['cycle_free']}."
    )
    return 0 if report["cycle_free"] else 1
