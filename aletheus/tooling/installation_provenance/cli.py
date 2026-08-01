from __future__ import annotations

import argparse
from pathlib import Path

from .engine import Engine


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("append",), nargs="?", default="append")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/installation_provenance"),
    )
    args = parser.parse_args()
    installer = Path("aletheus/tooling/genesis_installer/engine.py")
    entry = Engine(args.output).append(
        release="20.3",
        commit="current",
        installer=installer,
        certification="certified",
        rollback_point="current-head",
        runtime_compatibility="compatible",
    )
    print(f"Installation Provenance complete: release={entry['release']}.")
    return 0
