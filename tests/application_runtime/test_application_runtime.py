from __future__ import annotations

import pytest

from aletheus.application_runtime import (
    ApplicationStatus,
    ConstitutionalApplicationRuntime,
    ConstitutionalProofApplication,
    DuplicateApplicationError,
    InvalidApplicationTransitionError,
)
from aletheus.platform_surface import (
    build_aletheus_platform,
)


def build_runtime():
    platform = build_aletheus_platform()

    runtime = ConstitutionalApplicationRuntime(
        platform=platform
    )

    return runtime, platform


def test_installs_constitutional_application():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()

    record = runtime.install(application)

    assert record.status == (
        ApplicationStatus.INSTALLED
    )
    assert (
        record.manifest.application_id
        == "aletheus.proof_application"
    )


def test_rejects_duplicate_application():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()

    runtime.install(application)

    with pytest.raises(
        DuplicateApplicationError
    ):
        runtime.install(
            ConstitutionalProofApplication()
        )


def test_injects_platform_surface_services():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()

    runtime.install(application)
    record = runtime.initialize(
        application.manifest.application_id
    )

    assert record.status == (
        ApplicationStatus.INITIALIZED
    )

    assert set(application.services) == {
        "runtime",
        "security",
        "cases",
        "missions",
        "ledger",
    }


def test_runs_complete_application_lifecycle():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()
    application_id = (
        application.manifest.application_id
    )

    runtime.install(application)
    runtime.initialize(application_id)
    runtime.start(application_id)

    assert application.running
    assert (
        runtime.registry.require(
            application_id
        ).status
        == ApplicationStatus.RUNNING
    )

    runtime.stop(application_id)

    assert not application.running
    assert (
        runtime.registry.require(
            application_id
        ).status
        == ApplicationStatus.STOPPED
    )


def test_application_cannot_start_before_initialize():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()
    application_id = (
        application.manifest.application_id
    )

    runtime.install(application)

    with pytest.raises(
        InvalidApplicationTransitionError
    ):
        runtime.start(application_id)


def test_application_health_is_projected():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()
    application_id = (
        application.manifest.application_id
    )

    runtime.install(application)
    runtime.initialize(application_id)
    runtime.start(application_id)

    health = runtime.application_health(
        application_id
    )

    assert health["status"] == "running"
    assert health["runtime_status"] == "online"
    assert health["details"]["initialized"]
    assert health["details"]["running"]


def test_uninstalls_stopped_application():
    runtime, _ = build_runtime()
    application = ConstitutionalProofApplication()
    application_id = (
        application.manifest.application_id
    )

    runtime.install(application)
    runtime.initialize(application_id)
    runtime.start(application_id)
    runtime.stop(application_id)

    removed = runtime.uninstall(
        application_id
    )

    assert removed.status == (
        ApplicationStatus.UNINSTALLED
    )
    assert runtime.registry.get(
        application_id
    ) is None
