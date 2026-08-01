from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import RuntimeExplorer


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m aletheus.tooling.runtime_explorer")
    parser.add_argument("command", choices=("node", "impact"))
    parser.add_argument("--node", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument(
        "--twin",
        type=Path,
        default=Path(
            "reports/architecture/kinekt/twin/architectural-digital-twin.json"
        ),
    )
    args = parser.parse_args()
    explorer = RuntimeExplorer(args.twin)
    result = (
        explorer.node(args.node)
        if args.command == "node"
        else explorer.impact(args.node, args.depth)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result is not None else 1
