from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

CONTRACT = (
    ROOT
    / "nimble"
    / "governance"
    / "deployment"
    / "deployment-contract.json"
)

BUILD_METADATA = (
    ROOT
    / "nimble"
    / "governance"
    / "deployment"
    / "build-metadata.json"
)

REPORT = (
    ROOT
    / "reports"
    / "nimble"
    / "deployment-readiness-latest.json"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def validate_backend_module(
    module_reference: str,
) -> list[str]:
    failures: list[str] = []

    if ":" not in module_reference:
        return [
            "Backend module must use module:attribute format."
        ]

    module_name, attribute = module_reference.split(
        ":",
        1,
    )

    try:
        module = importlib.import_module(module_name)
    except Exception as error:
        return [
            "Backend module import failed: "
            f"{type(error).__name__}: {error}"
        ]

    if not hasattr(module, attribute):
        failures.append(
            f"Backend module has no {attribute!r} attribute."
        )

    return failures


def validate_environment(
    contract: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    for requirement in contract.get(
        "required_environment",
        [],
    ):
        name = requirement["name"]
        value = os.environ.get(name)

        if requirement.get("required") and not value:
            failures.append(
                f"Required environment variable is missing: {name}"
            )
            continue

        allowed = requirement.get("allowed_values")

        if value and allowed and value not in allowed:
            failures.append(
                f"{name} has unsupported value: {value}"
            )

    for conditional in contract.get(
        "conditional_environment",
        [],
    ):
        condition = conditional.get("when", {})

        applies = all(
            os.environ.get(name) == value
            for name, value in condition.items()
        )

        if not applies:
            continue

        for requirement in conditional.get(
            "required",
            [],
        ):
            name = requirement["name"]

            if not os.environ.get(name):
                failures.append(
                    "Conditional environment variable "
                    f"is missing: {name}"
                )

    return failures


def validate_probe_contract(
    contract: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    probes = contract.get("probes", {})

    for probe_name in ("liveness", "readiness"):
        probe = probes.get(probe_name)

        if not probe:
            failures.append(
                f"Missing {probe_name} probe contract."
            )
            continue

        path = probe.get("path", "")

        if not re.fullmatch(
            r"/[A-Za-z0-9/_-]+",
            path,
        ):
            failures.append(
                f"Invalid {probe_name} probe path: {path}"
            )

        if probe.get("expected_status") != 200:
            failures.append(
                f"{probe_name} expected status must be 200."
            )

    return failures


def main() -> int:
    failures: list[str] = []

    for required in (
        CONTRACT,
        BUILD_METADATA,
    ):
        if not required.exists():
            failures.append(
                "Missing deployment evidence: "
                f"{required.relative_to(ROOT)}"
            )

    if failures:
        for failure in failures:
            print("FAIL:", failure)
        return 1

    contract = load_json(CONTRACT)
    metadata = load_json(BUILD_METADATA)

    expected_contract_hash = (
        metadata["deployment_contract"]["sha256"]
    )

    actual_contract_hash = sha256_file(CONTRACT)

    if expected_contract_hash != actual_contract_hash:
        failures.append(
            "Deployment contract changed without "
            "regenerating build metadata."
        )

    frontend_distribution = (
        ROOT
        / contract["service"][
            "frontend_distribution"
        ]
    )

    if not frontend_distribution.exists():
        failures.append(
            "Frontend production distribution is missing."
        )

    failures.extend(
        validate_backend_module(
            contract["service"]["backend_module"]
        )
    )

    failures.extend(
        validate_environment(contract)
    )

    failures.extend(
        validate_probe_contract(contract)
    )

    report = {
        "schema_version": "1.0",
        "status": "PASS" if not failures else "FAIL",
        "backend_module": contract["service"][
            "backend_module"
        ],
        "frontend_distribution": contract["service"][
            "frontend_distribution"
        ],
        "auth_mode": os.environ.get(
            "ALETHEUS_AUTH_MODE"
        ),
        "probes": contract["probes"],
        "failures": failures,
    }

    REPORT.write_text(
        json.dumps(
            report,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ DEPLOYMENT READINESS")
    print("=" * 72)
    print("Auth mode:", report["auth_mode"])
    print(
        "Backend module:",
        report["backend_module"],
    )
    print(
        "Frontend distribution:",
        report["frontend_distribution"],
    )

    for failure in failures:
        print("FAIL:", failure)

    print("Status:", report["status"])

    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
