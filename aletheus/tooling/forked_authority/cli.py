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
        default=Path("reports/architecture/kinekt/forked_authority"),
    )
    args = parser.parse_args()
    root = Path("reports/architecture/kinekt")
    report = Engine(
        root / "claim_envelopes/ambivalent-claim-envelopes.json",
        root / "flow_state_envelope/flow-state-envelope.json",
        args.output,
    ).build()
    print(f"Forked Authority Resolution complete: forks={report['fork_count']}.")
    return 0
