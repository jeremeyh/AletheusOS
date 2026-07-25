#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _find_repo_root() -> Path:
    current = Path(__file__).resolve().parent

    while True:
        if (current / "pyproject.toml").is_file():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root."
            )

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

LEDGER_PATH = (
    ROOT
    / "nimble"
    / "governance"
    / "audit"
    / "deployment-audit-ledger.jsonl"
)

LATEST_POINTER_PATH = (
    ROOT
    / "nimble"
    / "governance"
    / "audit"
    / "checkpoints"
    / "latest.json"
)

SIGNED_ANCHOR_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "signed-audit-anchor.json"
)

PLAN_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "recovery"
    / "audit-recovery-plan-latest.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def canonical_bytes(
    payload: dict[str, Any],
) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def calculate_hash(
    payload: dict[str, Any],
) -> str:
    return hashlib.sha256(
        canonical_bytes(payload)
    ).hexdigest()


def run_validator(script_name: str) -> dict[str, Any]:
    result = subprocess.run(
        ["python", script_name],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
    )

    return {
        "script": script_name,
        "returncode": result.returncode,
        "status": (
            "PASS"
            if result.returncode == 0
            else "FAIL"
        ),
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def read_ledger() -> tuple[
    list[dict[str, Any]],
    list[str],
]:
    failures: list[str] = []
    entries: list[dict[str, Any]] = []

    if not LEDGER_PATH.is_file():
        failures.append(
            "Deployment audit ledger is missing."
        )
        return entries, failures

    expected_previous_hash = "GENESIS"

    for line_number, line in enumerate(
        LEDGER_PATH.read_text(
            encoding="utf-8"
        ).splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            failures.append(
                f"Ledger line {line_number}: invalid JSON: "
                f"{error}"
            )
            continue

        expected_sequence = len(entries) + 1

        if event.get("sequence") != expected_sequence:
            failures.append(
                f"Ledger entry {expected_sequence}: "
                "sequence mismatch."
            )

        if (
            event.get("previous_hash")
            != expected_previous_hash
        ):
            failures.append(
                f"Ledger entry {expected_sequence}: "
                "previous_hash mismatch."
            )

        recorded_hash = event.get("event_hash")

        payload_without_hash = {
            key: value
            for key, value in event.items()
            if key != "event_hash"
        }

        calculated_hash = calculate_hash(
            payload_without_hash
        )

        if recorded_hash != calculated_hash:
            failures.append(
                f"Ledger entry {expected_sequence}: "
                "event_hash mismatch."
            )

        entries.append(event)
        expected_previous_hash = recorded_hash

    return entries, failures


def resolve_checkpoint_path(
    pointer: dict[str, Any],
) -> Path:
    raw_path = pointer.get("checkpoint_path")

    if not isinstance(raw_path, str):
        raise RuntimeError(
            "Latest checkpoint pointer has no valid path."
        )

    relative_path = Path(raw_path)

    if relative_path.is_absolute():
        raise RuntimeError(
            "Absolute checkpoint paths are forbidden."
        )

    if ".." in relative_path.parts:
        raise RuntimeError(
            "Checkpoint path traversal is forbidden."
        )

    checkpoint_path = (ROOT / relative_path).resolve()

    checkpoint_root = (
        ROOT
        / "nimble/governance/audit/checkpoints"
    ).resolve()

    if checkpoint_root not in checkpoint_path.parents:
        raise RuntimeError(
            "Checkpoint is outside the governed directory."
        )

    if not checkpoint_path.is_file():
        raise RuntimeError(
            "Checkpoint target is missing."
        )

    return checkpoint_path


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        default=str(PLAN_PATH),
    )

    arguments = parser.parse_args()

    output_path = Path(arguments.output)

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    failures: list[str] = []

    contract = load_json(CONTRACT_PATH)

    validations = [
        run_validator(
            "bin/validate_nimble_audit_ledger.py"
        ),
        run_validator(
            "bin/validate_nimble_audit_checkpoints.py"
        ),
        run_validator(
            "bin/validate_nimble_signed_audit_anchor.py"
        ),
    ]

    pointer = load_json(
        LATEST_POINTER_PATH
    )

    checkpoint_path = resolve_checkpoint_path(
        pointer
    )

    checkpoint = load_json(checkpoint_path)
    anchor = load_json(SIGNED_ANCHOR_PATH)
    anchor_subject = anchor.get("subject", {})

    checkpoint_hash = checkpoint.get(
        "checkpoint_hash"
    )

    checkpoint_entry_count = checkpoint.get(
        "ledger_entry_count"
    )

    checkpoint_head_hash = checkpoint.get(
        "ledger_head_hash"
    )

    required_bindings = {
        "checkpoint_hash": checkpoint_hash,
        "ledger_entry_count": checkpoint_entry_count,
        "ledger_head_hash": checkpoint_head_hash,
        "git_revision": checkpoint.get(
            "git_revision"
        ),
        "release_identity": checkpoint.get(
            "release_identity"
        ),
    }

    binding_checks: list[dict[str, Any]] = []

    for name, expected_value in (
        required_bindings.items()
    ):
        actual_value = anchor_subject.get(name)
        passed = actual_value == expected_value

        binding_checks.append(
            {
                "binding": name,
                "status": (
                    "PASS" if passed else "FAIL"
                ),
                "expected": expected_value,
                "actual": actual_value,
            }
        )

        if not passed:
            failures.append(
                f"Signed-anchor binding mismatch: {name}"
            )

    if pointer.get(
        "checkpoint_hash"
    ) != checkpoint_hash:
        failures.append(
            "Latest pointer does not bind the "
            "resolved checkpoint."
        )

    ledger, ledger_failures = read_ledger()
    failures.extend(ledger_failures)

    current_entry_count = len(ledger)

    current_head_hash = (
        ledger[-1].get("event_hash")
        if ledger
        else "GENESIS"
    )

    anchored_prefix_hash: str | None

    if checkpoint_entry_count == 0:
        anchored_prefix_hash = "GENESIS"
    elif (
        isinstance(checkpoint_entry_count, int)
        and checkpoint_entry_count <= len(ledger)
    ):
        anchored_prefix_hash = ledger[
            checkpoint_entry_count - 1
        ].get("event_hash")
    else:
        anchored_prefix_hash = None

    signed_anchor_failed = any(
        item["script"]
        == "bin/validate_nimble_signed_audit_anchor.py"
        and item["status"] == "FAIL"
        for item in validations
    )

    if signed_anchor_failed or failures:
        classification = "untrusted_source"
        recommended_action = (
            "manual_forensic_review"
        )

    elif current_entry_count < checkpoint_entry_count:
        classification = "checkpoint_ahead_of_ledger"
        recommended_action = (
            "restore_missing_suffix"
        )

    elif anchored_prefix_hash != checkpoint_head_hash:
        classification = "diverged_before_checkpoint"
        recommended_action = (
            "manual_forensic_review"
        )

    else:
        classification = "healthy"
        recommended_action = "none"

    plan_without_hash: dict[str, Any] = {
        "schema_version": "1.0",
        "contract_id": contract["contract_id"],
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "mode": "plan_only",
        "classification": classification,
        "recommended_action": recommended_action,
        "mutation_performed": false_value(),
        "trusted_checkpoint": {
            "path": checkpoint_path.relative_to(
                ROOT
            ).as_posix(),
            "checkpoint_sequence": checkpoint.get(
                "checkpoint_sequence"
            ),
            "checkpoint_hash": checkpoint_hash,
            "ledger_entry_count": (
                checkpoint_entry_count
            ),
            "ledger_head_hash": (
                checkpoint_head_hash
            ),
            "git_revision": checkpoint.get(
                "git_revision"
            ),
            "release_identity": checkpoint.get(
                "release_identity"
            ),
        },
        "current_ledger": {
            "path": LEDGER_PATH.relative_to(
                ROOT
            ).as_posix(),
            "entry_count": current_entry_count,
            "head_hash": current_head_hash,
            "anchored_prefix_hash": (
                anchored_prefix_hash
            ),
        },
        "validation_results": validations,
        "binding_checks": binding_checks,
        "failures": failures,
        "next_requirements": {
            "pre_recovery_snapshot_required": (
                recommended_action
                == "restore_missing_suffix"
            ),
            "explicit_apply_command_required": (
                recommended_action
                == "restore_missing_suffix"
            ),
            "automatic_mutation_forbidden": True,
        },
    }

    plan_hash = calculate_hash(
        plan_without_hash
    )

    plan = {
        **plan_without_hash,
        "plan_hash": plan_hash,
    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            plan,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    status = (
        "PASS"
        if recommended_action == "none"
        else "REVIEW_REQUIRED"
    )

    print("=" * 72)
    print("NIMBLEâ¢ AUDIT RECOVERY PLAN")
    print("=" * 72)
    print(f"Classification: {classification}")
    print(
        "Recommended action:",
        recommended_action,
    )
    print(
        "Current ledger entries:",
        current_entry_count,
    )
    print(
        "Checkpoint entries:",
        checkpoint_entry_count,
    )
    print("Mutation performed: False")
    print(f"Plan hash: {plan_hash}")
    print(
        "Plan:",
        output_path.relative_to(ROOT),
    )
    print(f"Status: {status}")

    return (
        0
        if recommended_action == "none"
        else 2
    )


def false_value() -> bool:
    return False


if __name__ == "__main__":
    raise SystemExit(main())

