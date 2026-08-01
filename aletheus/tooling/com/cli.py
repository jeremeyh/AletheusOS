from __future__ import annotations

import argparse
from pathlib import Path

from .engine import CognitiveMeshEngine


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.com")
    parser.add_argument("command", choices=("analyze",), nargs="?", default="analyze")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("reports/architecture/kinekt/com-input.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/com"),
    )
    args = parser.parse_args()

    if not args.input.exists():
        args.input.parent.mkdir(parents=True, exist_ok=True)
        args.input.write_text('{"contributions": []}', encoding="utf-8")

    report = CognitiveMeshEngine(args.input, args.output).analyze()
    print(
        "COM complete: "
        f"contributions={len(report.contributions)}, "
        f"consensus={len(report.consensus)}, "
        f"unresolved={len(report.unresolved_topics)}."
    )
    return 0
