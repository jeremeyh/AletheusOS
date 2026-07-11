from __future__ import annotations

import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

DEPLOY_ADAPTER = (
    ROOT / "scripts/nimble_deploy_adapter.sh"
)

ROLLBACK_ADAPTER = (
    ROOT / "scripts/nimble_rollback_adapter.sh"
)


def run_adapter(
    path: Path,
    environment: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(path)],
        cwd=ROOT,
        env={
            **os.environ,
            **environment,
        },
        capture_output=True,
        text=True,
        check=False,
    )


def test_deploy_adapter_supports_dry_run() -> None:
    result = run_adapter(
        DEPLOY_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "dry-run",
            "NIMBLE_ENVIRONMENT": "staging",
            "NIMBLE_RELEASE": "release-v1",
            "NIMBLE_REVISION": "abc123",
            "NIMBLE_IMAGE": "example/image@sha256:test",
        },
    )

    assert result.returncode == 0
    assert "deployment dry run" in result.stdout


def test_deploy_adapter_fails_closed_without_command() -> None:
    result = run_adapter(
        DEPLOY_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "execute",
            "NIMBLE_ENVIRONMENT": "production",
            "NIMBLE_RELEASE": "release-v1",
            "NIMBLE_REVISION": "abc123",
            "NIMBLE_IMAGE": "example/image@sha256:test",
            "NIMBLE_DEPLOY_COMMAND": "",
        },
    )

    assert result.returncode != 0
    assert "requires NIMBLE_DEPLOY_COMMAND" in result.stderr


def test_rollback_adapter_fails_closed_without_command() -> None:
    result = run_adapter(
        ROLLBACK_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "execute",
            "NIMBLE_ENVIRONMENT": "production",
            "ROLLBACK_RELEASE": "release-v0",
            "ROLLBACK_REVISION": "def456",
            "ROLLBACK_IMAGE": "example/image@sha256:rollback",
            "NIMBLE_ROLLBACK_COMMAND": "",
        },
    )

    assert result.returncode != 0
    assert "NIMBLE_ROLLBACK_COMMAND" in result.stderr
