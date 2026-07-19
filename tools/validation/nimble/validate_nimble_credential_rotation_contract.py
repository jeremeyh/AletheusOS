#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


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
    "credential-rotation-contract-latest.json"
)


def main() -> int:
    failures: list[str] = []

    for path in [
        CONTRACT_PATH,
        METADATA_PATH,
        REVOCATION_PATH,
    ]:
        if not path.is_file():
            failures.append(
                f"Missing credential governance file: "
                f"{path.relative_to(ROOT)}"
            )

    if failures:
        status = "FAIL"
    else:
        contract = json.loads(
            CONTRACT_PATH.read_text(
                encoding="utf-8"
            )
        )

        policy = contract.get("policy", {})

        required_true = [
            "rotation_required",
            "issued_at_required",
            "expires_at_required",
            "fingerprint_required",
            "stale_credentials_forbidden",
            "expired_credentials_forbidden",
            "revoked_credentials_forbidden",
            "lineage_required_after_rotation",
            "raw_secret_values_forbidden",
            "fail_closed",
        ]

        for name in required_true:
            if policy.get(name) is not True:
                failures.append(
                    f"Rotation policy must be true: {name}"
                )

        thresholds = contract.get(
            "thresholds",
            {},
        )

        max_age = thresholds.get(
            "default_max_age_days"
        )

        warning = thresholds.get(
            "warning_before_expiry_days"
        )

        critical = thresholds.get(
            "critical_before_expiry_days"
        )

        if (
            not isinstance(max_age, int)
            or max_age <= 0
        ):
            failures.append(
                "default_max_age_days must be positive."
            )

        if (
            not isinstance(warning, int)
            or warning <= 0
        ):
            failures.append(
                "warning_before_expiry_days "
                "must be positive."
            )

        if (
            not isinstance(critical, int)
            or critical <= 0
        ):
            failures.append(
                "critical_before_expiry_days "
                "must be positive."
            )

        if (
            isinstance(warning, int)
            and isinstance(critical, int)
            and critical >= warning
        ):
            failures.append(
                "Critical expiry threshold must be "
                "less than warning threshold."
            )

        status = (
            "PASS"
            if not failures
            else "FAIL"
        )

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "status": status,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ CREDENTIAL ROTATION CONTRACT")
    print("=" * 72)
    print(f"Status: {status}")
    print(f"Failures: {len(failures)}")
    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
