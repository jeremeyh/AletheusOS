from __future__ import annotations

import argparse
from pathlib import Path

from .engine import ExperienceDistributionEngine


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genesis 37.21 experience distribution runtime"
    )
    parser.add_argument("--write-plan", type=Path)
    parser.add_argument("--validate-root", type=Path)
    args = parser.parse_args()

    engine = ExperienceDistributionEngine()

    if args.write_plan:
        engine.write_plan(args.write_plan)
        print(f"Distribution plan written to {args.write_plan}")

    if args.validate_root:
        errors = engine.validate_distribution_root(args.validate_root)
        if errors:
            for error in errors:
                print(f"ERROR: {error}")
            return 1
        print("Distribution root is valid.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
