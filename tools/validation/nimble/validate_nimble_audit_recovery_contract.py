#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


def _find_repo_root() -> Path:
    current = Path(__file__).resolve().parent

    while True:
        contract = (
            current
            / "nimble"
            / "governance"
            / "audit"
            / "recovery"
            / "audit-recovery-contract.json"
        )

        if contract.is_file():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = _find_repo_root()

CONTRACT_PATH = (
    ROOT
    / "nimble"
    / "governance"
    / "audit"
    / "recovery"
    / "audit-recovery-contract.json"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "recovery"
    / "audit-recovery-contract-validation-latest.json"
)


def main() -> int:
    failures: list[str] = []

    if not CONTRACT_PATH.is_file():
        failures.append("Audit recovery contract is missing.")
        contract = {}
    else:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    if contract.get("mode") != "plan_only":
        failures.append("Recovery must default to plan_only mode.")

    policy = contract.get("policy", {})

    required_policy = [
        "automatic_ledger_mutation_forbidden",
        "recovery_plan_required",
        "checkpoint_validation_required",
        "signed_anchor_validation_required",
        "ledger_prefix_validation_required",
        "checkpoint_hash_binding_required",
        "ledger_head_binding_required",
        "ledger_entry_count_binding_required",
        "git_revision_binding_required",
        "release_identity_binding_required",
        "ambiguous_source_rejection_required",
        "pre_recovery_snapshot_required_before_apply",
        "recovery_provenance_required",
        "absolute_paths_forbidden",
    ]

    for key in required_policy:
        if policy.get(key) is not True:
            failures.append(f"Recovery policy must be true: {key}")

    apply_policy = contract.get("apply", {})

    if apply_policy.get("confirmation_token") != "APPLY-AUDIT-RECOVERY":
        failures.append("Recovery confirmation token is invalid.")

    required_apply_policy = [
        "atomic_replacement_required",
        "source_revalidation_required",
        "plan_hash_validation_required",
        "pre_recovery_snapshot_required",
        "post_recovery_validation_required",
        "recovery_audit_event_required",
    ]

    for key in required_apply_policy:
        if apply_policy.get(key) is not True:
            failures.append(f"Recovery apply policy must be true: {key}")

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

    if failures:
        print("Status: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Status: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
