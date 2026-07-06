import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aletheus.council import CouncilEngine


def main():
    parser = argparse.ArgumentParser(description="Council™ governance review")
    parser.add_argument("--proposal", default="General architecture review")
    parser.add_argument("--source", default="manual")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = CouncilEngine(ROOT).review(
        proposal=args.proposal,
        source=args.source,
    )

    council = result["council"]
    decision = council["decision"]

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print()
    print("=" * 72)
    print("Council™")
    print("=" * 72)
    print(f"Version    : {council['version']}")
    print(f"Proposal   : {council['proposal']}")
    print(f"Approved   : {decision['approved']}")
    print(f"Mode       : {decision['mode']}")
    print(f"Confidence : {decision['confidence']}")
    print(f"PrincipleX : {decision['principle_x']}")
    print("=" * 72)


if __name__ == "__main__":
    main()
