#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import uuid
from datetime import UTC, datetime
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
            raise RuntimeError(
                "Unable to locate repository root."
            )

        probe = probe.parent


ROOT = _find_root()


LEDGER_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

LATEST_POINTER_PATH = (
    ROOT
    / "nimble/governance/audit/checkpoints/"
    "latest.json"
)

DEFAULT_OUTPUT_PATH = (
    ROOT
    / "reports/nimble/recovery/"
    "trusted-audit-recovery-source.json"
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
    return hashlib.sha256(
        canonical_json_bytes(payload)
    ).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def read_ledger() -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in LEDGER_PATH.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


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


def resolve_checkpoint() -> dict[str, Any]:
    pointer = read_json(
        LATEST_POINTER_PATH
    )

    raw_path = pointer.get("checkpoint_path")

    if not isinstance(raw_path, str):
        raise RuntimeError(
            "Latest checkpoint path is invalid."
        )

    relative_path = Path(raw_path)

    if (
        relative_path.is_absolute()
        or ".." in relative_path.parts
    ):
        raise RuntimeError(
            "Checkpoint path violates policy."
        )

    checkpoint_path = (
        ROOT / relative_path
    ).resolve()

    governed_root = (
        ROOT
        / "nimble/governance/audit/checkpoints"
    ).resolve()

    if governed_root not in checkpoint_path.parents:
        raise RuntimeError(
            "Checkpoint is outside its governed directory."
        )

    checkpoint = read_json(checkpoint_path)

    if (
        pointer.get("checkpoint_hash")
        != checkpoint.get("checkpoint_hash")
    ):
        raise RuntimeError(
            "Checkpoint pointer binding mismatch."
        )

    return checkpoint


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_PATH),
    )

    arguments = parser.parse_args()

    output_path = Path(arguments.output)

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    ledger = read_ledger()
    checkpoint = resolve_checkpoint()

    checkpoint_entry_count = checkpoint.get(
        "ledger_entry_count"
    )

    if not isinstance(
        checkpoint_entry_count,
        int,
    ):
        raise RuntimeError(
            "Checkpoint entry count is invalid."
        )

    if len(ledger) < checkpoint_entry_count:
        raise RuntimeError(
            "Canonical ledger is shorter than "
            "the latest checkpoint."
        )

    anchored_hash = (
        "GENESIS"
        if checkpoint_entry_count == 0
        else ledger[
            checkpoint_entry_count - 1
        ].get("event_hash")
    )

    if anchored_hash != checkpoint.get(
        "ledger_head_hash"
    ):
        raise RuntimeError(
            "Canonical ledger does not match "
            "the checkpoint prefix."
        )

    ledger_bytes = ledger_jsonl_bytes(ledger)

    payload_without_hash: dict[str, Any] = {
        "schema_version": "1.0",
        "source_id": str(uuid.uuid4()),
        "created_at": datetime.now(
            UTC
        ).isoformat(),
        "checkpoint_hash": checkpoint.get(
            "checkpoint_hash"
        ),
        "checkpoint_entry_count": (
            checkpoint_entry_count
        ),
        "checkpoint_head_hash": checkpoint.get(
            "ledger_head_hash"
        ),
        "ledger_entry_count": len(ledger),
        "ledger_file_sha256": hashlib.sha256(
            ledger_bytes
        ).hexdigest(),
        "ledger_entries": ledger,
    }

    source = {
        **payload_without_hash,
        "source_hash": calculate_hash(
            payload_without_hash
        ),
    }

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_text(
        json.dumps(
            source,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ AUDIT RECOVERY SOURCE")
    print("=" * 72)
    print(
        f"Ledger entries: {len(ledger)}"
    )
    print(
        "Checkpoint entries:",
        checkpoint_entry_count,
    )
    print(
        "Checkpoint hash:",
        checkpoint.get("checkpoint_hash"),
    )
    print(
        "Source hash:",
        source["source_hash"],
    )
    print(
        "Source:",
        output_path.relative_to(ROOT),
    )
    print("Status: PASS")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
