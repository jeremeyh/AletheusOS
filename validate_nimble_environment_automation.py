#!/usr/bin/env python3

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

CONTRACT_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "environment-promotion-contract.json"
)

STAGING_WORKFLOW = (
    ROOT
    / ".github/workflows/"
    "nimble-staging-promotion.yml"
)

PRODUCTION_WORKFLOW = (
    ROOT
    / ".github/workflows/"
    "nimble-production-promotion.yml"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "environment-automation-validation-latest.json"
)


def record(
    checks: list[dict[str, Any]],
    failures: list[str],
    name: str,
    passed: bool,
    detail: str,
) -> None:
    checks.append(
        {
            "check": name,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
        }
    )

    if not passed:
        failures.append(detail)


def main() -> int:
    checks: list[dict[str, Any]] = []
    failures: list[str] = []

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    workflows = {
        "staging": STAGING_WORKFLOW,
        "production": PRODUCTION_WORKFLOW,
    }

    for environment, path in workflows.items():
        exists = path.is_file()

        record(
            checks,
            failures,
            f"{environment}-workflow-exists",
            exists,
            f"Missing workflow: {path.relative_to(ROOT)}",
        )

        if not exists:
            continue

        text = path.read_text(encoding="utf-8")

        expected_environment = contract[
            "environments"
        ][environment]["github_environment"]

        record(
            checks,
            failures,
            f"{environment}-environment-binding",
            (
                f"name: {expected_environment}"
                in text
            ),
            (
                f"{environment} workflow must bind "
                f"to {expected_environment}."
            ),
        )

        expected_concurrency = contract[
            "environments"
        ][environment]["deployment_concurrency"]

        record(
            checks,
            failures,
            f"{environment}-concurrency",
            (
                f"group: {expected_concurrency}"
                in text
            ),
            (
                f"{environment} workflow must use "
                f"concurrency group {expected_concurrency}."
            ),
        )

        record(
            checks,
            failures,
            f"{environment}-health-check",
            "curl" in text and "health" in text.lower(),
            (
                f"{environment} workflow requires "
                "post-deploy health verification."
            ),
        )

    production_text = PRODUCTION_WORKFLOW.read_text(
        encoding="utf-8",
    )

    adapter_requirements = {
        "deployment-adapter-script": (
            ROOT / "scripts/nimble_deploy_adapter.sh"
        ).is_file(),
        "rollback-adapter-script": (
            ROOT / "scripts/nimble_rollback_adapter.sh"
        ).is_file(),
        "adapter-contract": (
            ROOT
            / "nimble/governance/environments/"
            "deployment-adapter-contract.json"
        ).is_file(),
        "staging-adapter-call": (
            "./scripts/nimble_deploy_adapter.sh"
            in STAGING_WORKFLOW.read_text(
                encoding="utf-8"
            )
        ),
        "production-adapter-call": (
            "./scripts/nimble_deploy_adapter.sh"
            in production_text
        ),
        "production-rollback-call": (
            "./scripts/nimble_rollback_adapter.sh"
            in production_text
        ),
    }

    for name, passed in adapter_requirements.items():
        record(
            checks,
            failures,
            name,
            passed,
            f"Environment automation missing: {name}.",
        )

    production_requirements = {
        "rollback-release-input": (
            "rollback_release:" in production_text
        ),
        "rollback-revision-input": (
            "rollback_revision:" in production_text
        ),
        "rollback-image-input": (
            "rollback_image:" in production_text
        ),
        "staging-evidence-input": (
            "staging_run_id:" in production_text
        ),
        "rollback-execution": (
            "Execute rollback adapter"
            in production_text
        ),
        "staging-artifact-download": (
            "actions/download-artifact@v4"
            in production_text
        ),
    }

    for name, passed in production_requirements.items():
        record(
            checks,
            failures,
            name,
            passed,
            f"Production workflow missing: {name}.",
        )

    forbidden = re.findall(
        r"\brun:\s*(?:kubectl|helm|aws|gcloud|az)\b",
        production_text,
    )

    record(
        checks,
        failures,
        "provider-neutral-adapter",
        not forbidden,
        (
            "Provider-specific deployment commands "
            "must remain outside the governance workflow."
        ),
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
    print("NIMBLE™ ENVIRONMENT AUTOMATION")
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
