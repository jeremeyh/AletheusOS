from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

REGISTRY_PATH = (
    ROOT
    / "nimble/governance/environments/"
    "deployment-provider-registry.json"
)

DISPATCHER = (
    ROOT / "scripts/nimble_provider_dispatch.py"
)


def load_registry() -> dict:
    return json.loads(
        REGISTRY_PATH.read_text(encoding="utf-8")
    )


def run_dispatcher(
    provider: str,
    action: str = "deploy",
    environment: str = "staging",
) -> subprocess.CompletedProcess[str]:
    runtime_environment = {
        **os.environ,
        "NIMBLE_DEPLOY_MODE": "dry-run",
        "NIMBLE_DEPLOY_PROVIDER": provider,
        "NIMBLE_RELEASE": "release-v1",
        "NIMBLE_REVISION": "abc123",
        "NIMBLE_IMAGE": "example/image@sha256:test",
        "ROLLBACK_RELEASE": "release-v0",
        "ROLLBACK_REVISION": "def456",
        "ROLLBACK_IMAGE": "example/image@sha256:rollback",
    }

    return subprocess.run(
        [
            "python",
            str(DISPATCHER),
            "--provider",
            provider,
            "--action",
            action,
            "--environment",
            environment,
        ],
        cwd=ROOT,
        env=runtime_environment,
        capture_output=True,
        text=True,
        check=False,
    )


def test_registry_exists() -> None:
    assert REGISTRY_PATH.is_file()


def test_default_provider_is_registered() -> None:
    registry = load_registry()

    assert (
        registry["default_provider"]
        in registry["providers"]
    )


def test_provider_executables_are_repository_relative() -> None:
    registry = load_registry()

    for provider in registry["providers"].values():
        executable = Path(provider["executable"])

        assert not executable.is_absolute()
        assert ".." not in executable.parts


def test_dry_run_provider_dispatches_deploy() -> None:
    result = run_dispatcher("dry-run")

    assert result.returncode == 0
    assert "Action: deploy" in result.stdout


def test_dry_run_provider_dispatches_rollback() -> None:
    result = run_dispatcher(
        "dry-run",
        action="rollback",
        environment="production",
    )

    assert result.returncode == 0
    assert "Action: rollback" in result.stdout


def test_unregistered_provider_fails_closed() -> None:
    result = run_dispatcher("unregistered-provider")

    assert result.returncode != 0

    combined = result.stdout + result.stderr

    assert "Unregistered deployment provider" in combined


def test_dry_run_provider_cannot_execute_production() -> None:
    runtime_environment = {
        **os.environ,
        "NIMBLE_DEPLOY_MODE": "execute",
        "NIMBLE_RELEASE": "release-v1",
        "NIMBLE_REVISION": "abc123",
        "NIMBLE_IMAGE": "example/image@sha256:test",
    }

    result = subprocess.run(
        [
            "python",
            str(DISPATCHER),
            "--provider",
            "dry-run",
            "--action",
            "deploy",
            "--environment",
            "production",
        ],
        cwd=ROOT,
        env=runtime_environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode != 0

    combined = result.stdout + result.stderr

    assert "not approved for production execution" in combined
