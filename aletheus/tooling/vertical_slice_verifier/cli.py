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
        default=Path("reports/architecture/kinekt/vertical_slice_verification"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "path_resolver/end-to-end-path-resolver.json",
        root / "touchpoints/platform-touchpoint-matrix.json",
        args.output,
    ).build()
    print(
        f"Vertical Slice Verification complete: connected={report['top_to_bottom_connected']}."
    )
    return 0
