from __future__ import annotations

import argparse
import json

from .engine import RuntimeRealizationEngine
from .models import EvidenceNode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true")
    args = parser.parse_args()
    if args.demo:
        nodes = [
            EvidenceNode("verified", 1.0, 0.99, 1.0, 0.99),
            EvidenceNode("hypothesis", 0.55, 0.48, 0.7, 0.42, 0.6),
        ]
        print(json.dumps(RuntimeRealizationEngine().score_nodes(nodes), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
