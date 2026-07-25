#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def find_repo_root(start: Path) -> Path:
    current = start.resolve()

    while True:
        if (current / "pyproject.toml").exists():
            return current

        if current.parent == current:
            raise RuntimeError("Unable to locate repository root.")

        current = current.parent


ROOT = find_repo_root(Path(__file__).parent)


CONTRACT_PATH = (
    ROOT
    / "nimble/governance/release/"
    "promotion-contract.json"
)

PROMOTION_PATH = (
    ROOT
    / "reports/nimble/"
    "nimble-promotion-record.json"
)

REPORT_PATH = (
    ROOT
    / "reports/nimble/"
    "promotion-validation-latest.json"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def write_report(
    payload: dict[str, Any],
) -> None:
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    REPORT_PATH.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--environment",
        choices=[
            "build",
            "staging",
            "production",
        ],
    )

    arguments = parser.parse_args()

    failures: list[str] = []
    checks: list[dict[str, Any]] = []

    if not CONTRACT_PATH.is_file():
        failures.append(
            "Promotion contract is missing."
        )

    if not PROMOTION_PATH.is_file():
        failures.append(
            "Promotion record is missing."
        )

    if failures:
        write_report(
            {
                "schema_version": "1.0",
                "generated_at": datetime.now(
                    UTC
                ).isoformat(),
                "status": "FAIL",
                "checks": checks,
                "failures": failures,
            }
        )

        return 1

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    promotion = json.loads(
        PROMOTION_PATH.read_text(
            encoding="utf-8",
        )
    )

    environment = promotion.get("environment")

    if (
        arguments.environment
        and arguments.environment != environment
    ):
        failures.append(
            "Promotion environment does not match "
            "the requested validation environment."
        )

    if environment not in contract[
        "promotion_sequence"
    ]:
        failures.append(
            f"Unknown promotion environment: {environment!r}"
        )

    candidate = promotion.get(
        "candidate",
        {},
    )

    current_revision = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()

    revision_matches = (
        candidate.get("revision")
        == current_revision
    )

    checks.append(
        {
            "check": "candidate-revision",
            "status": (
                "PASS"
                if revision_matches
                else "FAIL"
            ),
        }
    )

    if not revision_matches:
        failures.append(
            "Promotion candidate revision does not "
            "match HEAD."
        )

    evidence_records = (
        promotion.get(
            "integrity",
            {},
        ).get("evidence", [])
    )

    evidence_by_name = {
        record.get("name"): record
        for record in evidence_records
        if isinstance(record, dict)
    }

    required_names = {
        "build": {
            "release_manifest",
            "release_manifest_checksum",
            "release_integrity_report",
        },
        "staging": {
            "release_manifest",
            "release_manifest_checksum",
            "release_integrity_report",
            "deployment_readiness",
            "image_provenance_contract",
        },
        "production": {
            "release_manifest",
            "release_manifest_checksum",
            "release_integrity_report",
            "deployment_readiness",
            "image_provenance_contract",
            "image_identity",
            "image_digest",
            "sbom",
            "container_smoke",
        },
    }.get(environment, set())

    for name in sorted(required_names):
        record = evidence_by_name.get(name)

        if not record:
            failures.append(
                f"Required promotion evidence missing: {name}"
            )
            continue

        relative_path = record.get("path", "")

        if (
            not isinstance(relative_path, str)
            or relative_path.startswith("/")
            or ".." in Path(relative_path).parts
        ):
            failures.append(
                f"Invalid evidence path: {relative_path!r}"
            )
            continue

        path = ROOT / relative_path

        present = path.is_file()

        checks.append(
            {
                "check": f"evidence:{name}",
                "status": (
                    "PASS"
                    if present
                    else "FAIL"
                ),
            }
        )

        if not present:
            failures.append(
                f"Evidence file is missing: {relative_path}"
            )
            continue

        expected_digest = record.get("sha256")
        actual_digest = sha256_file(path)

        if expected_digest != actual_digest:
            failures.append(
                f"Evidence checksum mismatch: {relative_path}"
            )

    if environment == "production":
        tags = candidate.get("tags") or []

        if not tags:
            failures.append(
                "Production promotion requires a tag."
            )

        rollback = promotion.get(
            "rollback",
            {},
        )

        rollback_release = rollback.get("release")
        rollback_revision = rollback.get("revision")

        if not rollback_release:
            failures.append(
                "Production promotion requires "
                "a rollback release."
            )

        if not rollback_revision:
            failures.append(
                "Production promotion requires "
                "a rollback revision."
            )

        if rollback_revision == current_revision:
            failures.append(
                "Rollback revision must differ from "
                "the candidate revision."
            )

    status = "PASS" if not failures else "FAIL"

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.now(
            UTC
        ).isoformat(),
        "environment": environment,
        "candidate_revision": current_revision,
        "status": status,
        "checks": checks,
        "failures": failures,
    }

    write_report(report)

    print("=" * 72)
    print("NIMBLE™ RELEASE PROMOTION VALIDATION")
    print("=" * 72)
    print(f"Environment: {environment}")
    print(f"Revision: {current_revision}")
    print(f"Status: {status}")
    print(f"Failures: {len(failures)}")
    if status == "PASS":
        subprocess.run(
            [
                "python",
                str(ROOT / "append_nimble_audit_event.py"),
                "--event-type",
                "promotion_validated",
                "--environment",
                str(environment),
                "--release",
                str(
                    candidate.get(
                        "release",
                        "unknown",
                    )
                ),
                "--revision",
                current_revision,
                "--metadata-json",
                json.dumps(
                    {
                        "rollback_required": (
                            environment == "production"
                        ),
                    }
                ),
            ],
            cwd=ROOT,
            check=True,
        )

    print(
        "Report:",
        REPORT_PATH.relative_to(ROOT),
    )

    for failure in failures:
        print(f"- {failure}")

    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
