import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from aletheus.platform import PlatformLayer


def main():
    parser = argparse.ArgumentParser(description="AletheusOS Platform Layer inspection")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = PlatformLayer(ROOT).inspect()
    platform_result = result["platform"]

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print()
    print("=" * 72)
    print("AletheusOS Platform Layer™")
    print("=" * 72)
    print(f"Version : {platform_result['version']}")
    print(f"Status  : {platform_result['status']}")
    print(f"Score   : {platform_result['score']}")
    print(f"Root    : {platform_result['root']}")
    print("=" * 72)


if __name__ == "__main__":
    main()
