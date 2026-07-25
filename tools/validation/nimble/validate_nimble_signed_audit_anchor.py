#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
import re
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
    / "signed-audit-anchor-contract.json"
)

LATEST_POINTER = (
    ROOT
    / "nimble"
    / "governance"
    / "audit"
    / "checkpoints"
    / "latest.json"
)

ANCHOR_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "signed-audit-anchor.json"
)

CHECKSUM_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "signed-audit-anchor.sha256"
)

REPORT_PATH = (
    ROOT
    / "reports"
    / "nimble"
    / "signed-audit-anchor-validation-latest.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    required_paths = [
        CONTRACT_PATH,
        LATEST_POINTER,
        ANCHOR_PATH,
        CHECKSUM_PATH,
    ]

    for path in required_paths:
        if not path.is_file():
            failures.append(
                f"Missing signed-anchor file: "
                f"{path.relative_to(ROOT)}"
            )

    if failures:
        report = {
            "schema_version": "1.0",
            "generated_at": datetime.now(
                UTC
            ).isoformat(),
            "status": "FAIL",
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

        for failure in failures:
            print(f"- {failure}")

        return 1

    contract = load_json(CONTRACT_PATH)
    pointer = load_json(LATEST_POINTER)
    anchor = load_json(ANCHOR_PATH)

    subject = anchor.get("subject", {})
    checkpoint_value = subject.get(
        "checkpoint_path"
    )

    if not isinstance(checkpoint_value, str):
        failures.append(
            "Anchor checkpoint path is invalid."
        )
        checkpoint_path = None
    else:
        relative_path = Path(checkpoint_value)

        if (
            relative_path.is_absolute()
            or ".." in relative_path.parts
        ):
            failures.append(
                "Anchor checkpoint path violates policy."
            )
            checkpoint_path = None
        else:
            checkpoint_path = ROOT / relative_path

    if checkpoint_path is not None:
        if not checkpoint_path.is_file():
            failures.append(
                "Signed-anchor checkpoint subject "
                "is missing."
            )
        else:
            checkpoint = load_json(
                checkpoint_path
            )

            bindings = {
                "checkpoint_sequence": (
                    checkpoint.get(
                        "checkpoint_sequence"
                    )
                ),
                "checkpoint_hash": (
                    checkpoint.get(
                        "checkpoint_hash"
                    )
                ),
                "ledger_entry_count": (
                    checkpoint.get(
                        "ledger_entry_count"
                    )
                ),
                "ledger_head_hash": (
                    checkpoint.get(
                        "ledger_head_hash"
                    )
                ),
                "git_revision": (
                    checkpoint.get(
                        "git_revision"
                    )
                ),
                "release_identity": (
                    checkpoint.get(
                        "release_identity"
                    )
                ),
            }

            for key, expected_value in (
                bindings.items()
            ):
                passed = (
                    subject.get(key)
                    == expected_value
                )

                checks.append(
                    {
                        "check": (
                            f"checkpoint-binding:{key}"
                        ),
                        "status": (
                            "PASS"
                            if passed
                            else "FAIL"
                        ),
                    }
                )

                if not passed:
                    failures.append(
                        f"Checkpoint binding mismatch: "
                        f"{key}"
                    )

            checkpoint_digest = sha256_file(
                checkpoint_path
            )

            if (
                subject.get(
                    "checkpoint_file_sha256"
                )
                != checkpoint_digest
            ):
                failures.append(
                    "Checkpoint file digest mismatch."
                )

    if (
        subject.get("checkpoint_hash")
        != pointer.get("checkpoint_hash")
    ):
        failures.append(
            "Anchor does not bind the latest "
            "checkpoint pointer."
        )

    recorded_anchor_hash = anchor.get(
        "anchor_hash"
    )

    payload_without_hash = {
        key: value
        for key, value in anchor.items()
        if key != "anchor_hash"
    }

    calculated_anchor_hash = hashlib.sha256(
        canonical_bytes(payload_without_hash)
    ).hexdigest()

    if recorded_anchor_hash != calculated_anchor_hash:
        failures.append(
            "Signed-anchor internal hash mismatch."
        )

    checksum_line = CHECKSUM_PATH.read_text(
        encoding="utf-8",
    ).strip()

    checksum_match = re.fullmatch(
        r"([a-f0-9]{64})\s{2}"
        r"signed-audit-anchor\.json",
        checksum_line,
    )

    expected_file_digest = (
        checksum_match.group(1)
        if checksum_match
        else ""
    )

    actual_file_digest = sha256_file(
        ANCHOR_PATH
    )

    if expected_file_digest != actual_file_digest:
        failures.append(
            "Signed-anchor checksum mismatch."
        )

    signing_identity = anchor.get(
        "signing_identity",
        {},
    )

    if (
        signing_identity.get("provider")
        != contract["signing"]["provider"]
    ):
        failures.append(
            "Unexpected signing provider identity."
        )

    if (
        signing_identity.get(
            "expected_workflow"
        )
        != contract["signing"][
            "expected_workflow"
        ]
    ):
        failures.append(
            "Unexpected signing workflow identity."
        )

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "status": status,
        "checkpoint_hash": subject.get(
            "checkpoint_hash"
        ),
        "anchor_hash": recorded_anchor_hash,
        "anchor_file_sha256": actual_file_digest,
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

    print("=" * 72)
    print("NIMBLE™ SIGNED AUDIT ANCHOR")
    print("=" * 72)
    print(
        "Checkpoint hash:",
        subject.get("checkpoint_hash"),
    )
    print(f"Anchor hash: {recorded_anchor_hash}")
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
