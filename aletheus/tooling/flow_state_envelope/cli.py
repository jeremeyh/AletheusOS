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
        default=Path("reports/architecture/kinekt/flow_state_envelope"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "parallel_rails/parallel-rail-coordination.json",
        root / "claim_envelopes/ambivalent-claim-envelopes.json",
        args.output,
    ).build()
    print(
        f"Flow State Envelope complete: state={report['state']}, parallel={report['parallel_enabled']}."
    )
    return 0
