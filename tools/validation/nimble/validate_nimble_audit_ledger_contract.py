#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


CONTRACT_PATH = ROOT / "nimble/governance/audit/deployment-audit-ledger-contract.json"

LEDGER_PATH = ROOT / "nimble/governance/audit/deployment-audit-ledger.jsonl"

REPORT_PATH = ROOT / "reports/nimble/deployment-audit-ledger-contract-latest.json"


def main() -> int:
    failures: list[str] = []

    if not CONTRACT_PATH.is_file():
        failures.append("Audit ledger contract is missing.")

    if not LEDGER_PATH.is_file():
        failures.append("Audit ledger file is missing.")

    if not failures:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

        ledger = contract.get("ledger", {})
        policy = contract.get("policy", {})

        if ledger.get("format") != "jsonl":
            failures.append("Audit ledger format must be jsonl.")

        if ledger.get("append_only") is not True:
            failures.append("Audit ledger must be append-only.")

        if ledger.get("hash_algorithm") != "sha256":
            failures.append("Audit ledger hash must be sha256.")

        required_true = [
            "sequence_must_be_contiguous",
            "event_ids_must_be_unique",
            "timestamps_must_be_utc",
            "event_hash_required",
            "previous_hash_required",
            "tamper_detection_required",
            "raw_secret_values_forbidden",
            "raw_secret_names_forbidden",
            "absolute_paths_forbidden",
        ]

        for key in required_true:
            if policy.get(key) is not True:
                failures.append(f"Audit policy must be true: {key}")

    status = "PASS" if not failures else "FAIL"

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(UTC).isoformat(),
                "status": status,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ AUDIT LEDGER CONTRACT")
    print("=" * 72)
    print(f"Status: {status}")
    print(f"Failures: {len(failures)}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
