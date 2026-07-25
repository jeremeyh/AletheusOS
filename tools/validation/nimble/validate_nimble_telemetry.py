from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)

REPORT_DIRECTORY = ROOT / "reports" / "nimble"
LATEST_JSON = REPORT_DIRECTORY / "production-gate-latest.json"
LATEST_MARKDOWN = REPORT_DIRECTORY / "production-gate-latest.md"
HISTORY_JSONL = REPORT_DIRECTORY / "production-gate-history.jsonl"
LOG_FILE = REPORT_DIRECTORY / "production-gate-latest.log"

REQUIRED_TOP_LEVEL_KEYS = {
    "schema_version",
    "generated_at",
    "gate",
    "git",
    "runtime",
    "bundle",
    "environment",
}


def main() -> int:
    required_files = (
        LATEST_JSON,
        LATEST_MARKDOWN,
        HISTORY_JSONL,
        LOG_FILE,
    )

    missing = [
        path
        for path in required_files
        if not path.exists()
    ]

    if missing:
        for path in missing:
            print(
                "FAIL: Missing telemetry artifact:",
                path.relative_to(ROOT),
            )
        return 1

    report: dict[str, Any] = json.loads(
        LATEST_JSON.read_text(
            encoding="utf-8",
        )
    )

    missing_keys = (
        REQUIRED_TOP_LEVEL_KEYS
        - set(report)
    )

    if missing_keys:
        print(
            "FAIL: Missing report keys:",
            ", ".join(sorted(missing_keys)),
        )
        return 1

    gate = report["gate"]
    bundle = report["bundle"]

    if gate["status"] not in {
        "PASS",
        "FAIL",
    }:
        print(
            "FAIL: Invalid gate status:",
            gate["status"],
        )
        return 1

    if gate["duration_seconds"] < 0:
        print(
            "FAIL: Invalid gate duration."
        )
        return 1

    if not bundle["chunks"]:
        print(
            "FAIL: Bundle telemetry contains no chunks."
        )
        return 1

    if bundle["primary"] is None:
        print(
            "FAIL: Primary bundle telemetry is missing."
        )
        return 1

    history_lines = [
        line
        for line in HISTORY_JSONL.read_text(
            encoding="utf-8",
        ).splitlines()
        if line.strip()
    ]

    if not history_lines:
        print(
            "FAIL: Telemetry history is empty."
        )
        return 1

    json.loads(history_lines[-1])

    print("=" * 72)
    print("NIMBLE™ TELEMETRY VALIDATION")
    print("=" * 72)
    print("Latest JSON evidence: present")
    print("Markdown evidence: present")
    print("Raw gate log: present")
    print("Historical JSONL: present")
    print(
        "Gate status:",
        gate["status"],
    )
    print(
        "Gate duration:",
        f"{gate['duration_seconds']:.2f}s",
    )
    print(
        "Primary bundle:",
        f"{bundle['primary']['bytes']:,} bytes",
    )
    print(
        "Secondary chunks:",
        bundle["secondary_chunk_count"],
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
