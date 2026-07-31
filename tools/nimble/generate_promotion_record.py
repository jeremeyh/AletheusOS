#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent

CONTRACT_PATH = ROOT / "nimble/governance/release/promotion-contract.json"

RELEASE_MANIFEST_PATH = ROOT / "reports/nimble/nimble-release-manifest.json"

RELEASE_CHECKSUM_PATH = ROOT / "reports/nimble/nimble-release-manifest.sha256"

INTEGRITY_REPORT_PATH = ROOT / "reports/nimble/release-integrity-latest.json"

OUTPUT_PATH = ROOT / "reports/nimble/nimble-promotion-record.json"


def git(*arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    return result.stdout.strip()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def evidence_record(
    name: str,
    path: Path,
) -> dict[str, Any]:
    return {
        "name": name,
        "path": path.relative_to(ROOT).as_posix(),
        "present": path.is_file(),
        "sha256": (sha256_file(path) if path.is_file() else None),
    }


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--environment",
        required=True,
        choices=[
            "build",
            "staging",
            "production",
        ],
    )

    parser.add_argument(
        "--release",
        default=(
            os.environ.get("GITHUB_REF_NAME") or git("rev-parse", "--short=12", "HEAD")
        ),
    )

    parser.add_argument(
        "--rollback-release",
    )

    parser.add_argument(
        "--rollback-revision",
    )

    parser.add_argument(
        "--require-clean",
        action="store_true",
    )

    arguments = parser.parse_args()

    contract = json.loads(
        CONTRACT_PATH.read_text(
            encoding="utf-8",
        )
    )

    worktree = git("status", "--porcelain")

    if arguments.require_clean and worktree:
        raise RuntimeError("Promotion generation requires a clean worktree.")

    revision = git("rev-parse", "HEAD")

    tags = sorted(
        tag
        for tag in git(
            "tag",
            "--points-at",
            revision,
        ).splitlines()
        if tag
    )

    if arguments.environment == "production" and not tags:
        raise RuntimeError("Production promotion requires a release tag.")

    if arguments.environment == "production" and (
        not arguments.rollback_release or not arguments.rollback_revision
    ):
        raise RuntimeError(
            "Production promotion requires both "
            "--rollback-release and --rollback-revision."
        )

    if arguments.rollback_revision and arguments.rollback_revision == revision:
        raise RuntimeError("Rollback revision must differ from the candidate revision.")

    evidence = [
        evidence_record(
            "release_manifest",
            RELEASE_MANIFEST_PATH,
        ),
        evidence_record(
            "release_manifest_checksum",
            RELEASE_CHECKSUM_PATH,
        ),
        evidence_record(
            "release_integrity_report",
            INTEGRITY_REPORT_PATH,
        ),
        evidence_record(
            "deployment_readiness",
            ROOT / "nimble/governance/deployment/deployment-contract.json",
        ),
        evidence_record(
            "image_provenance_contract",
            ROOT / "nimble/governance/deployment/image-provenance-contract.json",
        ),
        evidence_record(
            "image_identity",
            ROOT / "reports/nimble/image-identity-latest.json",
        ),
        evidence_record(
            "image_digest",
            ROOT / "reports/nimble/image-digest-latest.json",
        ),
        evidence_record(
            "sbom",
            ROOT / "reports/nimble/nimble-image-sbom.spdx.json",
        ),
        evidence_record(
            "container_smoke",
            ROOT / "reports/nimble/container-smoke-latest.json",
        ),
    ]

    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "record_id": "nimble-promotion-record-v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "application": contract["application"],
        "environment": arguments.environment,
        "candidate": {
            "release": arguments.release,
            "revision": revision,
            "tags": tags,
        },
        "rollback": {
            "required": (arguments.environment == "production"),
            "release": arguments.rollback_release,
            "revision": arguments.rollback_revision,
        },
        "integrity": {
            "worktree_clean": not bool(worktree),
            "evidence": evidence,
        },
        "workflow": {
            "repository": os.environ.get(
                "GITHUB_REPOSITORY",
                "local",
            ),
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        },
    }

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_PATH.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=" * 72)
    print("NIMBLE™ RELEASE PROMOTION RECORD")
    print("=" * 72)
    print(f"Environment: {arguments.environment}")
    print(f"Release: {arguments.release}")
    print(f"Revision: {revision}")
    print(f"Tagged: {bool(tags)}")
    print(
        "Record:",
        OUTPUT_PATH.relative_to(ROOT),
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
