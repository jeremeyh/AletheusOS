#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
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
s[3]

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "audit-checkpoint-contract.json"
)

LEDGER_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

CHECKPOINT_DIRECTORY = (
    ROOT
    / "nimble/governance/audit/checkpoints"
)

LATEST_POINTER = CHECKPOINT_DIRECTORY / "latest.json"

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "audit-checkpoint-validation-latest.json"
)

SUMMARY_PATH = (
    ROOT
    / "reports/nimble/"
    "audit-checkpoint-summary-latest.json"
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


def read_ledger(
    failures: list[str],
) -> list[dict[str, Any]]:
    if not LEDGER_PATH.is_file():
        return []

    entries: list[dict[str, Any]] = []

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

    return entries


def main() -> int:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    checkpoint_paths = sorted(
        path
        for path in CHECKPOINT_DIRECTORY.glob(
            "checkpoint-*.json"
        )
        if path.is_file()
    )

    checkpoints: list[dict[str, Any]] = []

    for path in checkpoint_paths:
        try:
            checkpoint = json.loads(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except json.JSONDecodeError as error:
            failures.append(
                f"Invalid checkpoint JSON: {path.name}: {error}"
            )
            continue

        checkpoint["_path"] = path
        checkpoints.append(checkpoint)

    expected_previous_hash = contract[
        "checkpoint"
    ]["genesis_previous_checkpoint_hash"]

    previous_entry_count = -1

    for expected_sequence, checkpoint in enumerate(
        checkpoints,
        start=1,
    ):
        path = checkpoint.pop("_path")

        sequence = checkpoint.get(
            "checkpoint_sequence"
        )

        if sequence != expected_sequence:
            failures.append(
                f"{path.name}: checkpoint sequence "
                f"{sequence!r}, expected {expected_sequence}."
            )

        if (
            checkpoint.get("previous_checkpoint_hash")
            != expected_previous_hash
        ):
            failures.append(
                f"{path.name}: previous checkpoint "
                "hash mismatch."
            )

        recorded_hash = checkpoint.get(
            "checkpoint_hash"
        )

        payload_without_hash = {
            key: value
            for key, value in checkpoint.items()
            if key != "checkpoint_hash"
        }

        calculated_hash = calculate_hash(
            payload_without_hash
        )

        if recorded_hash != calculated_hash:
            failures.append(
                f"{path.name}: checkpoint hash mismatch."
            )

        entry_count = checkpoint.get(
            "ledger_entry_count"
        )

        if (
            not isinstance(entry_count, int)
            or entry_count < previous_entry_count
        ):
            failures.append(
                f"{path.name}: ledger entry count "
                "regressed."
            )

        previous_entry_count = (
            entry_count
            if isinstance(entry_count, int)
            else previous_entry_count
        )

        expected_previous_hash = recorded_hash

        checks.append(
            {
                "checkpoint_sequence": sequence,
                "checkpoint_hash": recorded_hash,
                "ledger_entry_count": entry_count,
                "status": "PASS",
            }
        )

        checkpoint["_path"] = path

    ledger = read_ledger(failures)

    ledger_entry_count = len(ledger)

    ledger_head_hash = (
        ledger[-1]["event_hash"]
        if ledger
        else "GENESIS"
    )

    if checkpoints:
        latest_checkpoint = checkpoints[-1]

        checkpoint_entry_count = latest_checkpoint.get(
            "ledger_entry_count"
        )

        checkpoint_head_hash = latest_checkpoint.get(
            "ledger_head_hash"
        )

        if ledger_entry_count < checkpoint_entry_count:
            failures.append(
                "Ledger truncation detected: current entry "
                "count is lower than the latest checkpoint."
            )
        elif ledger_entry_count == checkpoint_entry_count:
            if ledger_head_hash != checkpoint_head_hash:
                failures.append(
                    "Ledger rollback or replacement detected: "
                    "head hash differs from latest checkpoint."
                )
        else:
            anchored_index = checkpoint_entry_count - 1

            if checkpoint_entry_count == 0:
                anchored_hash = "GENESIS"
            elif anchored_index < len(ledger):
                anchored_hash = ledger[
                    anchored_index
                ].get("event_hash")
            else:
                anchored_hash = None

            if anchored_hash != checkpoint_head_hash:
                failures.append(
                    "Ledger history diverges from the "
                    "latest checkpoint."
                )

        if not LATEST_POINTER.is_file():
            failures.append(
                "Latest checkpoint pointer is missing."
            )
        else:
            pointer = json.loads(
                LATEST_POINTER.read_text(
                    encoding="utf-8"
                )
            )

            if (
                pointer.get("checkpoint_hash")
                != latest_checkpoint.get(
                    "checkpoint_hash"
                )
            ):
                failures.append(
                    "Latest pointer hash does not match "
                    "the newest checkpoint."
                )

            expected_path = latest_checkpoint[
                "_path"
            ].relative_to(ROOT).as_posix()

            if (
                pointer.get("checkpoint_path")
                != expected_path
            ):
                failures.append(
                    "Latest pointer path does not match "
                    "the newest checkpoint."
                )
    elif LATEST_POINTER.exists():
        failures.append(
            "Latest pointer exists without checkpoints."
        )

    status = "PASS" if not failures else "FAIL"

    latest_hash = (
        checkpoints[-1].get("checkpoint_hash")
        if checkpoints
        else contract["checkpoint"][
            "genesis_previous_checkpoint_hash"
        ]
    )

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "status": status,
        "checkpoint_count": len(checkpoints),
        "ledger_entry_count": ledger_entry_count,
        "ledger_head_hash": ledger_head_hash,
        "latest_checkpoint_hash": latest_hash,
        "checks": checks,
        "failures": failures,
    }

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    SUMMARY_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": report[
                    "generated_at"
                ],
                "status": status,
                "checkpoint_count": len(
                    checkpoints
                ),
                "latest_checkpoint_hash": (
                    latest_hash
                ),
                "ledger_entry_count": (
                    ledger_entry_count
                ),
                "ledger_head_hash": (
                    ledger_head_hash
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ AUDIT CHECKPOINT VALIDATION")
    print("=" * 72)
    print(f"Checkpoints: {len(checkpoints)}")
    print(f"Ledger entries: {ledger_entry_count}")
    print(f"Latest checkpoint: {latest_hash}")
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
