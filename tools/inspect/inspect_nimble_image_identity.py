#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONTRACT_PATH = (
    ROOT
    / "nimble/governance/deployment/"
    "image-provenance-contract.json"
)
IDENTITY_REPORT = (
    ROOT
    / "reports/nimble/"
    "image-identity-latest.json"
)
DIGEST_REPORT = (
    ROOT
    / "reports/nimble/"
    "image-digest-latest.json"
)


def run_json(command: list[str]) -> Any:
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )

    return json.loads(result.stdout)


def write_report(
    path: Path,
    payload: dict[str, Any],
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
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
        "--image",
        default=(
            "aletheus/"
            "nimble-experience-gateway:ci"
        ),
    )

    parser.add_argument(
        "--require-runtime",
        action="store_true",
    )

    arguments = parser.parse_args()

    docker = shutil.which("docker")

    generated_at = datetime.now(
        UTC
    ).isoformat()

    if docker is None:
        status = (
            "FAIL"
            if arguments.require_runtime
            else "SKIP"
        )

        payload = {
            "schema_version": "1.0",
            "generated_at": generated_at,
            "image": arguments.image,
            "status": status,
            "failures": (
                ["Docker runtime is unavailable."]
                if arguments.require_runtime
                else []
            ),
            "skip_reason": (
                "Docker runtime is unavailable."
            ),
        }

        write_report(
            IDENTITY_REPORT,
            payload,
        )

        write_report(
            DIGEST_REPORT,
            payload,
        )

        print("=" * 72)
        print("NIMBLE™ IMAGE IDENTITY INSPECTION")
        print("=" * 72)
        print("Docker runtime: unavailable")
        print(f"Status: {status}")

        return (
            1
            if arguments.require_runtime
            else 0
        )

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    inspect_data = run_json(
        [
            docker,
            "image",
            "inspect",
            arguments.image,
        ]
    )

    if not inspect_data:
        raise RuntimeError(
            "Docker returned no image inspection data."
        )

    image = inspect_data[0]
    labels = (
        image.get("Config", {}).get("Labels")
        or {}
    )

    failures: list[str] = []

    for label in contract["image"][
        "required_oci_labels"
    ]:
        value = labels.get(label)

        if not value:
            failures.append(
                f"Missing or empty OCI label: {label}"
            )

    configured_user = (
        image.get("Config", {}).get("User")
        or ""
    )

    expected_user = contract["image"][
        "runtime_user"
    ]

    if configured_user != expected_user:
        failures.append(
            "Unexpected runtime user: "
            f"{configured_user!r}; "
            f"expected {expected_user!r}."
        )

    image_id = str(
        image.get("Id", "")
    )

    if not image_id.startswith("sha256:"):
        failures.append(
            f"Image ID is not a sha256 digest: {image_id}"
        )

    repository_digests = (
        image.get("RepoDigests")
        or []
    )

    identity_status = (
        "PASS"
        if not failures
        else "FAIL"
    )

    identity_payload = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "image": arguments.image,
        "status": identity_status,
        "image_id": image_id,
        "runtime_user": configured_user,
        "labels": labels,
        "failures": failures,
    }

    digest_payload = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "image": arguments.image,
        "status": (
            "PASS"
            if image_id.startswith("sha256:")
            else "FAIL"
        ),
        "image_id": image_id,
        "repository_digests": repository_digests,
        "algorithm": "sha256",
    }

    write_report(
        IDENTITY_REPORT,
        identity_payload,
    )

    write_report(
        DIGEST_REPORT,
        digest_payload,
    )

    print("=" * 72)
    print("NIMBLE™ IMAGE IDENTITY INSPECTION")
    print("=" * 72)
    print(f"Image: {arguments.image}")
    print(f"Image ID: {image_id}")
    print(f"Runtime user: {configured_user}")
    print(f"Status: {identity_status}")

    for failure in failures:
        print(f"- {failure}")

    return (
        0
        if identity_status == "PASS"
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(main())
