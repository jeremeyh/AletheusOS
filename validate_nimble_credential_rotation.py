#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-rotation-contract.json"
)

METADATA_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-metadata.json"
)

REVOCATION_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "credential-revocations.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "credential-rotation-latest.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def parse_timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(
        value.replace("Z", "+00:00")
    )

    if parsed.tzinfo is None:
        raise ValueError(
            "Credential timestamp must include timezone."
        )

    return parsed.astimezone(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--provider",
        required=True,
    )

    parser.add_argument(
        "--environment",
        required=True,
        choices=["staging", "production"],
    )

    arguments = parser.parse_args()

    contract = load_json(CONTRACT_PATH)
    metadata = load_json(METADATA_PATH)
    revocations = load_json(REVOCATION_PATH)

    failures: list[str] = []
    warnings: list[str] = []
    checks: list[dict[str, Any]] = []

    now = datetime.now(timezone.utc)

    tolerance = timedelta(
        seconds=contract["thresholds"][
            "clock_skew_tolerance_seconds"
        ]
    )

    warning_window = timedelta(
        days=contract["thresholds"][
            "warning_before_expiry_days"
        ]
    )

    critical_window = timedelta(
        days=contract["thresholds"][
            "critical_before_expiry_days"
        ]
    )

    default_max_age = timedelta(
        days=contract["thresholds"][
            "default_max_age_days"
        ]
    )

    revoked_fingerprints = {
        record.get("fingerprint")
        for record in revocations.get(
            "revocations",
            [],
        )
        if isinstance(record, dict)
    }

    scoped_credentials = [
        record
        for record in metadata.get(
            "credentials",
            [],
        )
        if (
            record.get("provider")
            == arguments.provider
            and record.get("environment")
            == arguments.environment
        )
    ]

    for record in scoped_credentials:
        credential_id = record.get(
            "credential_id",
            "unknown",
        )

        fingerprint = record.get("fingerprint")
        issued_at_value = record.get("issued_at")
        expires_at_value = record.get("expires_at")

        if not fingerprint:
            failures.append(
                f"{credential_id}: fingerprint is missing."
            )
            continue

        if not issued_at_value:
            failures.append(
                f"{credential_id}: issued_at is missing."
            )
            continue

        if not expires_at_value:
            failures.append(
                f"{credential_id}: expires_at is missing."
            )
            continue

        try:
            issued_at = parse_timestamp(
                issued_at_value
            )
            expires_at = parse_timestamp(
                expires_at_value
            )
        except (TypeError, ValueError) as error:
            failures.append(
                f"{credential_id}: invalid timestamp: "
                f"{error}"
            )
            continue

        if issued_at > now + tolerance:
            failures.append(
                f"{credential_id}: issued_at is in "
                "the future."
            )

        if expires_at <= issued_at:
            failures.append(
                f"{credential_id}: expires_at must be "
                "later than issued_at."
            )

        if now >= expires_at:
            failures.append(
                f"{credential_id}: credential is expired."
            )

        age = now - issued_at

        max_age_days = record.get(
            "max_age_days",
            contract["thresholds"][
                "default_max_age_days"
            ],
        )

        try:
            max_age = timedelta(
                days=int(max_age_days)
            )
        except (TypeError, ValueError):
            failures.append(
                f"{credential_id}: invalid max_age_days."
            )
            max_age = default_max_age

        if age > max_age:
            failures.append(
                f"{credential_id}: credential exceeded "
                "its maximum rotation age."
            )

        remaining = expires_at - now

        if (
            timedelta(0)
            < remaining
            <= critical_window
        ):
            failures.append(
                f"{credential_id}: credential expires "
                "inside the critical window."
            )
        elif (
            timedelta(0)
            < remaining
            <= warning_window
        ):
            warnings.append(
                f"{credential_id}: credential expires "
                "inside the warning window."
            )

        if fingerprint in revoked_fingerprints:
            failures.append(
                f"{credential_id}: credential is revoked."
            )

        previous_fingerprint = record.get(
            "previous_fingerprint"
        )

        rotation_number = record.get(
            "rotation_number",
            1,
        )

        if (
            isinstance(rotation_number, int)
            and rotation_number > 1
            and not previous_fingerprint
        ):
            failures.append(
                f"{credential_id}: rotated credential "
                "lacks fingerprint lineage."
            )

        checks.append(
            {
                "credential_id": credential_id,
                "fingerprint": fingerprint,
                "rotation_number": rotation_number,
                "status": "PASS",
            }
        )

    status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    report = {
        "schema_version": "1.0",
        "generated_at": now.isoformat(),
        "provider": arguments.provider,
        "environment": arguments.environment,
        "credential_count": len(
            scoped_credentials
        ),
        "status": status,
        "checks": checks,
        "warnings": warnings,
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
    print("NIMBLE™ CREDENTIAL ROTATION")
    print("=" * 72)
    print(f"Provider: {arguments.provider}")
    print(f"Environment: {arguments.environment}")
    print(
        "Credentials:",
        len(scoped_credentials),
    )
    print(f"Warnings: {len(warnings)}")
    print(f"Failures: {len(failures)}")
    print(f"Status: {status}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for warning in warnings:
        print(f"WARNING: {warning}")

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
