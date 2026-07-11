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
    runtime_environment = {
        **os.environ,
        "NIMBLE_DEPLOY_PROVIDER": "dry-run",
        **environment,
    }

    return subprocess.run(
        [str(path)],
        cwd=ROOT,
        env=runtime_environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_deploy_adapter_supports_registered_dry_run() -> None:
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
    assert "registered provider dry run" in result.stdout
    assert "Action: deploy" in result.stdout
    assert "Environment: staging" in result.stdout


def test_deploy_adapter_rejects_unregistered_provider() -> None:
    result = run_adapter(
        DEPLOY_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "dry-run",
            "NIMBLE_DEPLOY_PROVIDER": "unregistered",
            "NIMBLE_ENVIRONMENT": "staging",
            "NIMBLE_RELEASE": "release-v1",
            "NIMBLE_REVISION": "abc123",
            "NIMBLE_IMAGE": "example/image@sha256:test",
        },
    )

    assert result.returncode != 0
    assert (
        "Unregistered deployment provider"
        in result.stderr
    )
    assert "Traceback" not in result.stderr


def test_dry_run_provider_cannot_execute_production() -> None:
    result = run_adapter(
        DEPLOY_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "execute",
            "NIMBLE_ENVIRONMENT": "production",
            "NIMBLE_RELEASE": "release-v1",
            "NIMBLE_REVISION": "abc123",
            "NIMBLE_IMAGE": "example/image@sha256:test",
        },
    )

    assert result.returncode != 0
    assert (
        "not approved for production execution"
        in result.stderr
    )
    assert "Traceback" not in result.stderr


def test_rollback_adapter_supports_registered_dry_run() -> None:
    result = run_adapter(
        ROLLBACK_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "dry-run",
            "NIMBLE_ENVIRONMENT": "production",
            "ROLLBACK_RELEASE": "release-v0",
            "ROLLBACK_REVISION": "def456",
            "ROLLBACK_IMAGE": (
                "example/image@sha256:rollback"
            ),
        },
    )

    assert result.returncode == 0
    assert "registered provider dry run" in result.stdout
    assert "Action: rollback" in result.stdout
    assert "Environment: production" in result.stdout


def test_rollback_adapter_rejects_unregistered_provider() -> None:
    result = run_adapter(
        ROLLBACK_ADAPTER,
        {
            "NIMBLE_DEPLOY_MODE": "dry-run",
            "NIMBLE_DEPLOY_PROVIDER": "unregistered",
            "NIMBLE_ENVIRONMENT": "production",
            "ROLLBACK_RELEASE": "release-v0",
            "ROLLBACK_REVISION": "def456",
            "ROLLBACK_IMAGE": (
                "example/image@sha256:rollback"
            ),
        },
    )

    assert result.returncode != 0
    assert (
        "Unregistered deployment provider"
        in result.stderr
    )
    assert "Traceback" not in result.stderr
