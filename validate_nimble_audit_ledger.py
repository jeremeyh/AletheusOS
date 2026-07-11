#!/usr/bin/env python3

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

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

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "deployment-audit-ledger-validation-latest.json"
)

SUMMARY_PATH = (
    ROOT
    / "reports/nimble/"
    "deployment-audit-ledger-summary-latest.json"
)


def canonical_payload(
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
        canonical_payload(payload)
    ).hexdigest()


def main() -> int:
    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    failures: list[str] = []
    checks: list[dict[str, Any]] = []
    entries: list[dict[str, Any]] = []

    if LEDGER_PATH.exists():
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
                failures.append(
                    f"Line {line_number}: invalid JSON: {error}"
                )

    event_ids: set[str] = set()
    expected_previous_hash = contract[
        "ledger"
    ]["genesis_previous_hash"]

    for index, event in enumerate(
        entries,
        start=1,
    ):
        sequence = event.get("sequence")

        if sequence != index:
            failures.append(
                f"Entry {index}: sequence is "
                f"{sequence!r}, expected {index}."
            )

        event_id = event.get("event_id")

        if not isinstance(event_id, str):
            failures.append(
                f"Entry {index}: missing event_id."
            )
        elif event_id in event_ids:
            failures.append(
                f"Entry {index}: duplicate event_id."
            )
        else:
            event_ids.add(event_id)

        if event.get("event_type") not in contract[
            "event_types"
        ]:
            failures.append(
                f"Entry {index}: unsupported event type."
            )

        if event.get(
            "previous_hash"
        ) != expected_previous_hash:
            failures.append(
                f"Entry {index}: previous_hash mismatch."
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
                f"Entry {index}: event_hash mismatch."
            )

        occurred_at = event.get("occurred_at")

        try:
            timestamp = datetime.fromisoformat(
                occurred_at.replace(
                    "Z",
                    "+00:00",
                )
            )

            if timestamp.tzinfo is None:
                raise ValueError(
                    "timestamp has no timezone"
                )
        except (
            AttributeError,
            TypeError,
            ValueError,
        ) as error:
            failures.append(
                f"Entry {index}: invalid occurred_at: "
                f"{error}"
            )

        checks.append(
            {
                "sequence": index,
                "event_type": event.get(
                    "event_type"
                ),
                "event_hash": recorded_hash,
                "status": "PASS",
            }
        )

        expected_previous_hash = recorded_hash

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "status": status,
        "entry_count": len(entries),
        "head_hash": (
            entries[-1].get("event_hash")
            if entries
            else contract["ledger"][
                "genesis_previous_hash"
            ]
        ),
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

    summary = {
        "schema_version": "1.0",
        "generated_at": report[
            "generated_at"
        ],
        "status": status,
        "entry_count": len(entries),
        "event_type_counts": {},
        "environment_counts": {},
        "head_hash": report["head_hash"],
    }

    for event in entries:
        event_type = str(
            event.get("event_type")
        )

        environment = str(
            event.get("environment")
        )

        summary["event_type_counts"][
            event_type
        ] = (
            summary["event_type_counts"].get(
                event_type,
                0,
            )
            + 1
        )

        summary["environment_counts"][
            environment
        ] = (
            summary["environment_counts"].get(
                environment,
                0,
            )
            + 1
        )

    SUMMARY_PATH.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ DEPLOYMENT AUDIT LEDGER")
    print("=" * 72)
    print(f"Entries: {len(entries)}")
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(f"Head hash: {report['head_hash']}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
