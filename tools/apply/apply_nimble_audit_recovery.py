#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

CONTRACT_PATH = ROOT / "nimble/governance/audit/recovery/audit-recovery-contract.json"

LEDGER_PATH = ROOT / "nimble/governance/audit/deployment-audit-ledger.jsonl"

DEFAULT_PLAN_PATH = ROOT / "reports/nimble/recovery/audit-recovery-plan-latest.json"

DEFAULT_SOURCE_PATH = (
    ROOT / "reports/nimble/recovery/trusted-audit-recovery-source.json"
)

SNAPSHOT_DIRECTORY = ROOT / "reports/nimble/recovery/snapshots"

SOURCE_VALIDATOR = ROOT / "validate_nimble_audit_recovery_source.py"

LEDGER_VALIDATOR = ROOT / "validate_nimble_audit_ledger.py"

AUDIT_WRITER = ROOT / "append_nimble_audit_event.py"


def canonical_bytes(payload: Any) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def calculate_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def run(
    command: list[str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=60,
        env={
            **os.environ,
            "PYTHONUNBUFFERED": "1",
        },
    )


def verify_plan(
    plan: dict[str, Any],
    contract: dict[str, Any],
) -> None:
    recorded_hash = plan.get("plan_hash")

    payload_without_hash = {
        key: value for key, value in plan.items() if key != "plan_hash"
    }

    calculated_hash = calculate_hash(payload_without_hash)

    if recorded_hash != calculated_hash:
        raise RuntimeError("Recovery plan hash mismatch.")

    expected_classification = contract["apply"]["recoverable_classification_required"]

    expected_action = contract["apply"]["recoverable_action_required"]

    if plan.get("classification") != expected_classification:
        raise RuntimeError(
            f"Recovery plan is not classified as {expected_classification}."
        )

    if plan.get("recommended_action") != expected_action:
        raise RuntimeError(f"Recovery plan does not authorize {expected_action}.")

    if plan.get("mutation_performed") is not False:
        raise RuntimeError("Recovery plan mutation state is invalid.")


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--plan",
        default=str(DEFAULT_PLAN_PATH),
    )

    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE_PATH),
    )

    parser.add_argument(
        "--confirm",
        required=True,
    )

    arguments = parser.parse_args()

    contract = load_json(CONTRACT_PATH)

    required_token = contract["apply"]["confirmation_token"]

    if arguments.confirm != required_token:
        raise RuntimeError(
            "Explicit recovery confirmation token is missing or invalid."
        )

    plan_path = Path(arguments.plan)
    source_path = Path(arguments.source)

    if not plan_path.is_absolute():
        plan_path = ROOT / plan_path

    if not source_path.is_absolute():
        source_path = ROOT / source_path

    if not plan_path.is_file():
        raise RuntimeError("Recovery plan is missing.")

    if not source_path.is_file():
        raise RuntimeError("Trusted recovery source is missing.")

    plan = load_json(plan_path)
    source = load_json(source_path)

    verify_plan(plan, contract)

    expected_checkpoint_hash = plan["trusted_checkpoint"]["checkpoint_hash"]

    if source.get("checkpoint_hash") != expected_checkpoint_hash:
        raise RuntimeError("Recovery source and plan bind different checkpoints.")

    SNAPSHOT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")

    snapshot_path = SNAPSHOT_DIRECTORY / f"deployment-audit-ledger-{timestamp}.jsonl"

    snapshot_metadata_path = (
        SNAPSHOT_DIRECTORY / f"deployment-audit-ledger-{timestamp}.metadata.json"
    )

    shutil.copy2(
        LEDGER_PATH,
        snapshot_path,
    )

    snapshot_hash = file_hash(snapshot_path)

    snapshot_metadata = {
        "schema_version": "1.0",
        "created_at": datetime.now(UTC).isoformat(),
        "snapshot_path": snapshot_path.relative_to(ROOT).as_posix(),
        "snapshot_sha256": snapshot_hash,
        "recovery_plan_hash": plan["plan_hash"],
        "recovery_source_hash": source["source_hash"],
        "checkpoint_hash": expected_checkpoint_hash,
    }

    snapshot_metadata_path.write_text(
        json.dumps(
            snapshot_metadata,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    with tempfile.TemporaryDirectory() as directory:
        reconstructed_path = Path(directory) / "reconstructed-ledger.jsonl"

        source_validation = run(
            [
                "python",
                str(SOURCE_VALIDATOR),
                "--source",
                str(source_path),
                "--output",
                str(reconstructed_path),
            ]
        )

        if source_validation.returncode != 0:
            raise RuntimeError(
                "Trusted recovery source validation failed:\n"
                + source_validation.stdout
                + source_validation.stderr
            )

        replacement_hash = file_hash(reconstructed_path)

        temporary_replacement = LEDGER_PATH.parent / (
            f".deployment-audit-ledger.{timestamp}.tmp"
        )

        shutil.copy2(
            reconstructed_path,
            temporary_replacement,
        )

        os.replace(
            temporary_replacement,
            LEDGER_PATH,
        )

    ledger_validation = run(
        [
            "python",
            str(LEDGER_VALIDATOR),
        ]
    )

    if ledger_validation.returncode != 0:
        shutil.copy2(
            snapshot_path,
            LEDGER_PATH,
        )

        raise RuntimeError(
            "Post-recovery ledger validation failed; "
            "the pre-recovery snapshot was restored.\n"
            + ledger_validation.stdout
            + ledger_validation.stderr
        )

    audit_event = run(
        [
            "python",
            str(AUDIT_WRITER),
            "--event-type",
            "audit_recovery_completed",
            "--environment",
            "governance",
            "--release",
            str(plan["trusted_checkpoint"]["release_identity"]),
            "--revision",
            str(plan["trusted_checkpoint"]["git_revision"]),
            "--metadata-json",
            json.dumps(
                {
                    "plan_hash": plan["plan_hash"],
                    "source_hash": source["source_hash"],
                    "checkpoint_hash": (expected_checkpoint_hash),
                    "snapshot_sha256": snapshot_hash,
                    "replacement_sha256": (replacement_hash),
                    "operator_confirmation": True,
                    "atomic_replacement": True,
                },
                sort_keys=True,
                separators=(",", ":"),
            ),
        ]
    )

    if audit_event.returncode != 0:
        raise RuntimeError(
            "Recovered ledger is valid, but recovery "
            "audit-event append failed:\n" + audit_event.stdout + audit_event.stderr
        )

    final_validation = run(
        [
            "python",
            str(LEDGER_VALIDATOR),
        ]
    )

    if final_validation.returncode != 0:
        raise RuntimeError(
            "Ledger failed validation after recovery "
            "provenance was appended.\n"
            + final_validation.stdout
            + final_validation.stderr
        )

    print("=" * 72)
    print("NIMBLE™ AUDIT RECOVERY APPLY")
    print("=" * 72)
    print(
        "Snapshot:",
        snapshot_path.relative_to(ROOT),
    )
    print(f"Snapshot SHA-256: {snapshot_hash}")
    print(f"Replacement SHA-256: {replacement_hash}")
    print("Atomic replacement: PASS")
    print("Post-recovery validation: PASS")
    print("Recovery provenance event: APPENDED")
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
