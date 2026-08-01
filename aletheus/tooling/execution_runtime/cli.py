from __future__ import annotations

import argparse
from pathlib import Path

from .engine import ExecutionRuntime


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("execute",), nargs="?", default="execute")
    parser.add_argument("--mission-id", default="genesis-19.1-smoke")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/architecture/kinekt/execution_runtime"),
    )
    args = parser.parse_args()
    runtime = ExecutionRuntime(
        Path(
            "reports/architecture/kinekt/process_composer/constitutional-process-composition.json"
        ),
        args.output,
    )
    result = runtime.execute_sync(args.mission_id, {"source": "cli"})
    runtime.write_result(result)
    print(
        "Constitutional Execution Runtime complete: "
        f"mission={result.mission_id}, status={result.status}, steps={len(result.steps)}."
    )
    return 0 if result.status == "completed" else 1
