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
    / "nimble/governance/deployment/"
    "image-provenance-contract.json"
)
REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "image-provenance-contract-latest.json"
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if not CONTRACT_PATH.exists():
        failures.append(
            f"Missing provenance contract: {CONTRACT_PATH}"
        )
        contract: dict[str, Any] = {}
    else:
        contract = load_json(CONTRACT_PATH)

    dockerfile_path = ROOT / str(
        contract.get("image", {}).get(
            "dockerfile",
            "Dockerfile.nimble",
        )
    )

    dockerfile_text = (
        dockerfile_path.read_text(encoding="utf-8")
        if dockerfile_path.exists()
        else ""
    )

    required_labels = contract.get(
        "image",
        {},
    ).get("required_oci_labels", [])

    for label in required_labels:
        present = label in dockerfile_text

        checks.append(
            {
                "check": f"oci-label:{label}",
                "status": "PASS" if present else "FAIL",
            }
        )

        if not present:
            failures.append(
                f"Missing OCI label in Dockerfile: {label}"
            )

    required_arguments = [
        "ALETHEUS_BUILD_VERSION",
        "ALETHEUS_BUILD_REVISION",
        "ALETHEUS_BUILD_CREATED",
        "ALETHEUS_BUILD_SOURCE",
        "ALETHEUS_BUILD_REF_NAME",
    ]

    for argument in required_arguments:
        pattern = rf"\bARG\s+{re.escape(argument)}\b"
        present = bool(
            re.search(
                pattern,
                dockerfile_text,
            )
        )

        checks.append(
            {
                "check": f"build-argument:{argument}",
                "status": "PASS" if present else "FAIL",
            }
        )

        if not present:
            failures.append(
                f"Missing Docker build argument: {argument}"
            )

    evidence = contract.get("evidence", {})

    for name, relative_path in evidence.items():
        valid = (
            isinstance(relative_path, str)
            and relative_path.startswith("reports/nimble/")
        )

        checks.append(
            {
                "check": f"evidence-path:{name}",
                "status": "PASS" if valid else "FAIL",
                "value": relative_path,
            }
        )

        if not valid:
            failures.append(
                f"Invalid evidence path for {name}: "
                f"{relative_path!r}"
            )

    sbom = contract.get("sbom", {})

    if sbom.get("format") != "spdx-json":
        failures.append(
            "SBOM format must be spdx-json."
        )

    if sbom.get("generator") != "syft":
        failures.append(
            "SBOM generator must be syft."
        )

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "contract": str(
            CONTRACT_PATH.relative_to(ROOT)
        ),
        "dockerfile": str(
            dockerfile_path.relative_to(ROOT)
        ),
        "status": status,
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
    print("NIMBLE™ IMAGE PROVENANCE CONTRACT")
    print("=" * 72)
    print(f"Status: {status}")
    print(f"Checks: {len(checks)}")
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
