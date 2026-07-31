#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _find_root() -> Path:
    current = Path(__file__).resolve().parent

    # Running from the isolated recovery simulation.
    if (current.parent / "nimble").is_dir():
        return current.parent

    # Running from the repository.
    probe = current
    while True:
        if (probe / "pyproject.toml").is_file():
            return probe

        if probe.parent == probe:
            raise RuntimeError("Unable to locate repository root.")

        probe = probe.parent


ROOT = _find_root()


LATEST_POINTER_PATH = ROOT / "nimble/governance/audit/checkpoints/latest.json"

DEFAULT_SOURCE_PATH = (
    ROOT / "reports/nimble/recovery/trusted-audit-recovery-source.json"
)

DEFAULT_OUTPUT_PATH = (
    ROOT / "reports/nimble/recovery/reconstructed-deployment-audit-ledger.jsonl"
)


def canonical_json_bytes(
    payload: Any,
) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def calculate_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def ledger_jsonl_bytes(
    entries: list[dict[str, Any]],
) -> bytes:
    if not entries:
        return b""

    return (
        "\n".join(
            json.dumps(
                entry,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            for entry in entries
        )
        + "\n"
    ).encode("utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_checkpoint() -> dict[str, Any]:
    pointer = load_json(LATEST_POINTER_PATH)

    raw_path = pointer.get("checkpoint_path")

    if not isinstance(raw_path, str):
        raise RuntimeError("Latest checkpoint path is invalid.")

    relative_path = Path(raw_path)

    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise RuntimeError("Checkpoint path violates policy.")

    checkpoint_path = ROOT / relative_path

    if not checkpoint_path.is_file():
        raise RuntimeError("Checkpoint target is missing.")

    checkpoint = load_json(checkpoint_path)

    if pointer.get("checkpoint_hash") != checkpoint.get("checkpoint_hash"):
        raise RuntimeError("Checkpoint pointer binding mismatch.")

    return checkpoint


def validate_chain(
    entries: list[dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    expected_previous_hash = "GENESIS"

    for expected_sequence, event in enumerate(
        entries,
        start=1,
    ):
        if event.get("sequence") != expected_sequence:
            failures.append(f"Entry {expected_sequence}: sequence mismatch.")

        if event.get("previous_hash") != expected_previous_hash:
            failures.append(f"Entry {expected_sequence}: previous_hash mismatch.")

        recorded_hash = event.get("event_hash")

        payload_without_hash = {
            key: value for key, value in event.items() if key != "event_hash"
        }

        calculated_hash = calculate_hash(payload_without_hash)

        if recorded_hash != calculated_hash:
            failures.append(f"Entry {expected_sequence}: event_hash mismatch.")

        expected_previous_hash = recorded_hash

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE_PATH),
    )

    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
    )

    parser.add_argument(
        "--no-write",
        action="store_true",
    )

    arguments = parser.parse_args()

    source_path = Path(arguments.source)
    output_path = Path(arguments.output)

    if not source_path.is_absolute():
        source_path = ROOT / source_path

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    source = load_json(source_path)
    checkpoint = resolve_checkpoint()

    failures: list[str] = []

    recorded_source_hash = source.get("source_hash")

    source_without_hash = {
        key: value for key, value in source.items() if key != "source_hash"
    }

    if recorded_source_hash != calculate_hash(source_without_hash):
        failures.append("Recovery source hash mismatch.")

    entries = source.get("ledger_entries")

    if not isinstance(entries, list):
        failures.append("Recovery source ledger_entries is invalid.")
        entries = []

    failures.extend(validate_chain(entries))

    ledger_bytes = ledger_jsonl_bytes(entries)

    if source.get("ledger_file_sha256") != hashlib.sha256(ledger_bytes).hexdigest():
        failures.append("Recovery source ledger digest mismatch.")

    bindings = {
        "checkpoint_hash": checkpoint.get("checkpoint_hash"),
        "checkpoint_entry_count": checkpoint.get("ledger_entry_count"),
        "checkpoint_head_hash": checkpoint.get("ledger_head_hash"),
    }

    for field, expected in bindings.items():
        if source.get(field) != expected:
            failures.append(f"Recovery source binding mismatch: {field}")

    checkpoint_entry_count = checkpoint.get("ledger_entry_count")

    if (
        isinstance(checkpoint_entry_count, int)
        and len(entries) >= checkpoint_entry_count
    ):
        anchored_hash = (
            "GENESIS"
            if checkpoint_entry_count == 0
            else entries[checkpoint_entry_count - 1].get("event_hash")
        )

        if anchored_hash != checkpoint.get("ledger_head_hash"):
            failures.append("Recovery source checkpoint prefix mismatch.")
    else:
        failures.append(
            "Recovery source does not contain the complete checkpoint prefix."
        )

    if failures:
        print("=" * 72)
        print("NIMBLE™ AUDIT RECOVERY SOURCE")
        print("=" * 72)
        print(f"Failures: {len(failures)}")
        print("Status: FAIL")

        for failure in failures:
            print(f"- {failure}")

        return 1

    mutation_performed = False

    if not arguments.no_write:
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_bytes(ledger_bytes)

    print("=" * 72)
    print("NIMBLE™ AUDIT RECOVERY SOURCE")
    print("=" * 72)
    print(f"Ledger entries: {len(entries)}")
    print(
        "Checkpoint prefix:",
        checkpoint_entry_count,
    )
    print(
        "Reconstruction written:",
        not arguments.no_write,
    )
    print(
        "Canonical ledger mutation:",
        mutation_performed,
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
