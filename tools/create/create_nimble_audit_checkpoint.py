#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]

CONTRACT_PATH = ROOT / "nimble/governance/audit/audit-checkpoint-contract.json"

LEDGER_PATH = ROOT / "nimble/governance/audit/deployment-audit-ledger.jsonl"

CHECKPOINT_DIRECTORY = ROOT / "nimble/governance/audit/checkpoints"

LATEST_POINTER = CHECKPOINT_DIRECTORY / "latest.json"


def git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


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
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def read_ledger() -> list[dict[str, Any]]:
    if not LEDGER_PATH.is_file():
        return []

    entries: list[dict[str, Any]] = []

    for line_number, line in enumerate(
        LEDGER_PATH.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise RuntimeError(f"Ledger line {line_number} is invalid JSON.") from error

    return entries


def load_previous_checkpoint() -> dict[str, Any] | None:
    if not LATEST_POINTER.is_file():
        return None

    pointer = json.loads(LATEST_POINTER.read_text(encoding="utf-8"))

    relative_path = pointer.get("checkpoint_path")

    if not isinstance(relative_path, str):
        raise RuntimeError("Latest checkpoint pointer is invalid.")

    checkpoint_path = ROOT / relative_path

    if not checkpoint_path.is_file():
        raise RuntimeError("Latest checkpoint target is missing.")

    return json.loads(checkpoint_path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--release",
        default=None,
    )

    parser.add_argument(
        "--require-clean",
        action="store_true",
    )

    arguments = parser.parse_args()

    release_identity = (
        arguments.release
        or os.environ.get("GITHUB_REF_NAME")
        or git("describe", "--tags", "--always")
    )

    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    worktree = git("status", "--porcelain")

    if arguments.require_clean and worktree:
        raise RuntimeError("Checkpoint creation requires a clean worktree.")

    ledger = read_ledger()

    ledger_entry_count = len(ledger)

    ledger_head_hash = ledger[-1]["event_hash"] if ledger else "GENESIS"

    previous_checkpoint = load_previous_checkpoint()

    previous_checkpoint_hash = (
        previous_checkpoint["checkpoint_hash"]
        if previous_checkpoint
        else contract["checkpoint"]["genesis_previous_checkpoint_hash"]
    )

    checkpoint_sequence = (
        int(previous_checkpoint["checkpoint_sequence"]) + 1
        if previous_checkpoint
        else 1
    )

    revision = git("rev-parse", "HEAD")

    tags = sorted(
        tag
        for tag in git(
            "tag",
            "--points-at",
            revision,
        ).splitlines()
        if tag
    )

    checkpoint_without_hash: dict[str, Any] = {
        "schema_version": "1.0",
        "checkpoint_sequence": checkpoint_sequence,
        "created_at": datetime.now(UTC).isoformat(),
        "ledger_entry_count": ledger_entry_count,
        "ledger_head_hash": ledger_head_hash,
        "git_revision": revision,
        "release_identity": release_identity,
        "git_tags": tags,
        "previous_checkpoint_hash": (previous_checkpoint_hash),
        "repository": os.environ.get(
            "GITHUB_REPOSITORY",
            "local",
        ),
        "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
    }

    checkpoint_hash = calculate_hash(checkpoint_without_hash)

    checkpoint = {
        **checkpoint_without_hash,
        "checkpoint_hash": checkpoint_hash,
    }

    CHECKPOINT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    checkpoint_filename = (
        f"checkpoint-{checkpoint_sequence:06d}-{checkpoint_hash[:16]}.json"
    )

    checkpoint_path = CHECKPOINT_DIRECTORY / checkpoint_filename

    if checkpoint_path.exists():
        raise RuntimeError("Checkpoint already exists; rewriting is forbidden.")

    checkpoint_path.write_text(
        json.dumps(
            checkpoint,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    pointer = {
        "schema_version": "1.0",
        "checkpoint_sequence": checkpoint_sequence,
        "checkpoint_hash": checkpoint_hash,
        "checkpoint_path": checkpoint_path.relative_to(ROOT).as_posix(),
    }

    LATEST_POINTER.write_text(
        json.dumps(
            pointer,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ AUDIT CHECKPOINT CREATED")
    print("=" * 72)
    print(f"Sequence: {checkpoint_sequence}")
    print(f"Ledger entries: {ledger_entry_count}")
    print(f"Ledger head: {ledger_head_hash}")
    print(f"Git revision: {revision}")
    print(f"Release: {release_identity}")
    print(f"Checkpoint hash: {checkpoint_hash}")
    print(
        "Checkpoint:",
        checkpoint_path.relative_to(ROOT),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
