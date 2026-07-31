#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _find_repo_root() -> Path:
    current = Path(__file__).resolve().parent

    while True:
        contract = (
            current
            / "nimble"
            / "governance"
            / "audit"
            / "signed-audit-anchor-contract.json"
        )

        if contract.is_file():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = _find_repo_root()

CONTRACT_PATH = ROOT / "nimble/governance/audit/signed-audit-anchor-contract.json"

LATEST_POINTER = ROOT / "nimble/governance/audit/checkpoints/latest.json"

ANCHOR_PATH = ROOT / "reports/nimble/signed-audit-anchor.json"

CHECKSUM_PATH = ROOT / "reports/nimble/signed-audit-anchor.sha256"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_bytes(
    payload: dict[str, Any],
) -> bytes:
    return (
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def resolve_checkpoint_path(
    pointer: dict[str, Any],
) -> Path:
    relative_value = pointer.get("checkpoint_path")

    if not isinstance(relative_value, str):
        raise RuntimeError("Latest checkpoint pointer has no valid path.")

    relative_path = Path(relative_value)

    if relative_path.is_absolute():
        raise RuntimeError("Absolute checkpoint paths are forbidden.")

    if ".." in relative_path.parts:
        raise RuntimeError("Checkpoint path traversal is forbidden.")

    checkpoint_path = (ROOT / relative_path).resolve()
    checkpoint_root = (ROOT / "nimble/governance/audit/checkpoints").resolve()

    if checkpoint_root not in checkpoint_path.parents:
        raise RuntimeError(
            "Checkpoint must remain inside the governed checkpoint directory."
        )

    if not checkpoint_path.is_file():
        raise RuntimeError("Latest checkpoint target is missing.")

    return checkpoint_path


def main() -> int:
    contract = load_json(CONTRACT_PATH)
    pointer = load_json(LATEST_POINTER)
    checkpoint_path = resolve_checkpoint_path(pointer)
    checkpoint = load_json(checkpoint_path)

    pointer_hash = pointer.get("checkpoint_hash")
    checkpoint_hash = checkpoint.get("checkpoint_hash")

    if pointer_hash != checkpoint_hash:
        raise RuntimeError("Latest pointer and checkpoint hash differ.")

    checkpoint_digest = sha256_file(checkpoint_path)

    payload_without_hash: dict[str, Any] = {
        "schema_version": "1.0",
        "anchor_id": "nimble-signed-audit-anchor-v0.1",
        "created_at": datetime.now(UTC).isoformat(),
        "subject": {
            "checkpoint_path": (checkpoint_path.relative_to(ROOT).as_posix()),
            "checkpoint_sequence": checkpoint.get("checkpoint_sequence"),
            "checkpoint_hash": checkpoint_hash,
            "checkpoint_file_sha256": (checkpoint_digest),
            "ledger_entry_count": checkpoint.get("ledger_entry_count"),
            "ledger_head_hash": checkpoint.get("ledger_head_hash"),
            "git_revision": checkpoint.get("git_revision"),
            "release_identity": checkpoint.get("release_identity"),
        },
        "signing_identity": {
            "provider": contract["signing"]["provider"],
            "expected_repository": os.environ.get(
                "GITHUB_REPOSITORY",
                "local",
            ),
            "expected_workflow": contract["signing"]["expected_workflow"],
            "workflow_run_id": os.environ.get("GITHUB_RUN_ID"),
            "workflow_run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        },
        "integrity": {
            "algorithm": "sha256",
            "latest_pointer_hash": pointer_hash,
        },
    }

    anchor_hash = sha256_bytes(canonical_bytes(payload_without_hash))

    payload = {
        **payload_without_hash,
        "anchor_hash": anchor_hash,
    }

    ANCHOR_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    anchor_bytes = canonical_bytes(payload)

    ANCHOR_PATH.write_bytes(anchor_bytes)

    anchor_file_digest = sha256_bytes(anchor_bytes)

    CHECKSUM_PATH.write_text(
        f"{anchor_file_digest}  {ANCHOR_PATH.name}\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ SIGNED AUDIT ANCHOR SUBJECT")
    print("=" * 72)
    print(
        "Checkpoint sequence:",
        checkpoint.get("checkpoint_sequence"),
    )
    print(f"Checkpoint hash: {checkpoint_hash}")
    print(
        "Checkpoint file SHA-256:",
        checkpoint_digest,
    )
    print(f"Anchor hash: {anchor_hash}")
    print(
        "Anchor file SHA-256:",
        anchor_file_digest,
    )
    print(
        "Anchor:",
        ANCHOR_PATH.relative_to(ROOT),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
