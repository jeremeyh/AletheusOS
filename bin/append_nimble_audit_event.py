#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import uuid
from datetime import datetime, timezone
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
            / "deployment-audit-ledger-contract.json"
        )

        if contract.is_file():
            return current

        if current.parent == current:
            raise RuntimeError(
                "Unable to locate repository root."
            )

        current = current.parent


ROOT = _find_repo_root()

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger-contract.json"
)

LEDGER_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "deployment-audit-ledger.jsonl"
)

FORBIDDEN_KEY_PATTERN = re.compile(
    r"(secret|password|token|credential)",
    re.IGNORECASE,
)


def load_contract() -> dict[str, Any]:
    return json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )


def read_entries() -> list[dict[str, Any]]:
    if not LEDGER_PATH.exists():
        return []

    entries: list[dict[str, Any]] = []

    for line_number, line in enumerate(
        LEDGER_PATH.read_text(
            encoding="utf-8"
        ).splitlines(),
        start=1,
    ):
        if not line.strip():
            continue

        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise RuntimeError(
                f"Ledger line {line_number} is invalid JSON: {error}"
            ) from error

    return entries


def canonical_payload(
    payload: dict[str, Any],
) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def event_hash(
    payload: dict[str, Any],
) -> str:
    return hashlib.sha256(
        canonical_payload(payload)
    ).hexdigest()


def validate_metadata(
    metadata: dict[str, Any],
) -> None:
    for key, value in metadata.items():
        if FORBIDDEN_KEY_PATTERN.search(key):
            raise RuntimeError(
                f"Sensitive metadata key is forbidden: {key}"
            )

        if isinstance(value, str):
            if value.startswith("/"):
                raise RuntimeError(
                    f"Absolute path forbidden in metadata: {key}"
                )

        if isinstance(value, dict):
            validate_metadata(value)


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--event-type",
        required=True,
    )

    parser.add_argument(
        "--environment",
        required=True,
    )

    parser.add_argument(
        "--release",
        required=True,
    )

    parser.add_argument(
        "--revision",
        required=True,
    )

    parser.add_argument(
        "--actor",
        default=(
            os.environ.get("GITHUB_ACTOR")
            or os.environ.get("USER")
            or "unknown"
        ),
    )

    parser.add_argument(
        "--metadata-json",
        default="{}",
    )

    arguments = parser.parse_args()

    contract = load_contract()

    if arguments.event_type not in contract[
        "event_types"
    ]:
        raise RuntimeError(
            f"Unsupported audit event type: "
            f"{arguments.event_type}"
        )

    metadata = json.loads(
        arguments.metadata_json
    )

    if not isinstance(metadata, dict):
        raise RuntimeError(
            "Audit metadata must be a JSON object."
        )

    validate_metadata(metadata)

    entries = read_entries()

    sequence = len(entries) + 1

    previous_hash = (
        entries[-1]["event_hash"]
        if entries
        else contract["ledger"][
            "genesis_previous_hash"
        ]
    )

    event_without_hash: dict[str, Any] = {
        "sequence": sequence,
        "event_id": str(uuid.uuid4()),
        "event_type": arguments.event_type,
        "occurred_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "actor": arguments.actor,
        "environment": arguments.environment,
        "release": arguments.release,
        "revision": arguments.revision,
        "previous_hash": previous_hash,
        "metadata": metadata,
    }

    digest = event_hash(
        event_without_hash
    )

    event = {
        **event_without_hash,
        "event_hash": digest,
    }

    LEDGER_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with LEDGER_PATH.open(
        "a",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json.dumps(
                event,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
            + "\n"
        )

    print("=" * 72)
    print("NIMBLE™ AUDIT EVENT APPENDED")
    print("=" * 72)
    print(f"Sequence: {sequence}")
    print(f"Event type: {arguments.event_type}")
    print(f"Environment: {arguments.environment}")
    print(f"Event hash: {digest}")
    print(
        "Ledger:",
        LEDGER_PATH.relative_to(ROOT),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
