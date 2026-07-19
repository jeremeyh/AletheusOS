#!/usr/bin/env python3

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

WORKFLOW_PATH = (
    ROOT
    / ".github/workflows/"
    "nimble-audit-anchor.yml"
)

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/audit/"
    "signed-audit-anchor-contract.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "signed-audit-anchor-workflow-latest.json"
)


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if not WORKFLOW_PATH.is_file():
        failures.append(
            "Signed-anchor workflow is missing."
        )
        workflow = ""
    else:
        workflow = WORKFLOW_PATH.read_text(
            encoding="utf-8"
        )

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8"
        )
    )

    required_tokens = {
        "attest-action": "uses: actions/attest@v4",
        "subject-path": (
            "subject-path: "
            "reports/nimble/signed-audit-anchor.json"
        ),
        "id-token-permission": "id-token: write",
        "attestations-permission": "attestations: write",
        "artifact-metadata-permission": (
            "artifact-metadata: write"
        ),
        "repository-verification": (
            '--repo "${GITHUB_REPOSITORY}"'
        ),
        "signer-workflow-verification": (
            '--signer-workflow "${SIGNER_WORKFLOW}"'
        ),
        "attestation-variable-guard": (
            "NIMBLE_ENABLE_ATTESTATIONS"
        ),
        "bundle-retention": (
            "signed-audit-anchor-attestation.json"
        ),
        "verification-retention": (
            "signed-audit-anchor-verification.json"
        ),
    }

    for name, token in required_tokens.items():
        passed = token in workflow

        checks.append(
            {
                "check": name,
                "status": (
                    "PASS" if passed else "FAIL"
                ),
            }
        )

        if not passed:
            failures.append(
                f"Signed-anchor workflow missing: {name}"
            )

    expected_workflow = contract[
        "signing"
    ]["expected_workflow"]

    actual_workflow = (
        WORKFLOW_PATH.relative_to(ROOT).as_posix()
    )

    if expected_workflow != actual_workflow:
        failures.append(
            "Contract workflow identity does not match "
            "the actual workflow path."
        )

    status = "PASS" if not failures else "FAIL"

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
                "checks": checks,
                "failures": failures,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ SIGNED ANCHOR WORKFLOW")
    print("=" * 72)
    print(f"Checks: {len(checks)}")
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
