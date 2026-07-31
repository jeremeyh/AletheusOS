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


CONTRACT_PATH = ROOT / "nimble/governance/audit/audit-checkpoint-contract.json"

REPORT_PATH = ROOT / "reports/nimble/audit-checkpoint-contract-latest.json"


def main() -> int:
    failures: list[str] = []

    if not CONTRACT_PATH.is_file():
        failures.append("Audit checkpoint contract is missing.")
    else:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

        checkpoint = contract.get(
            "checkpoint",
            {},
        )

        policy = contract.get(
            "policy",
            {},
        )

        if checkpoint.get("hash_algorithm") != "sha256":
            failures.append("Checkpoint hashing must use sha256.")

        required_true = [
            "checkpoint_chain_required",
            "ledger_head_binding_required",
            "git_revision_binding_required",
            "release_binding_required",
            "checkpoint_hash_required",
            "latest_pointer_required",
            "ledger_truncation_detection_required",
            "ledger_rollback_detection_required",
            "checkpoint_rewrite_forbidden",
            "absolute_paths_forbidden",
        ]

        for key in required_true:
            if policy.get(key) is not True:
                failures.append(f"Checkpoint policy must be true: {key}")

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
    print("NIMBLE™ AUDIT CHECKPOINT CONTRACT")
    print("=" * 72)
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
