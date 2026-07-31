from __future__ import annotations

from typing import Any

from aletheus.application_runtime import (
    ApplicationManifest,
    ConstitutionalApplicationRuntime,
)
from aletheus.platform_surface import (
    build_aletheus_platform,
)


class CognitiveHostedApplication:
    manifest = ApplicationManifest(
        application_id=("aletheus.cognitive_hosted_proof"),
        canonical_name=("Cognitive Hosted Proof™"),
        version="0.1.0",
        owner="6th Dimension Multimedia",
        purpose=("Prove injection of cognition, instrumentation, and scenarios."),
        required_services=(
            "cognition",
            "instrumentation",
            "scenarios",
        ),
        provided_capabilities=("cognitive_platform_proof",),
    )

    def __init__(self) -> None:
        self.services: dict[str, Any] = {}
        self.running = False

    def initialize(
        self,
        services: dict[str, Any],
    ) -> None:
        self.services = dict(services)

    def start(self) -> None:
        self.running = True

    def stop(self) -> None:
        self.running = False

    def health(self) -> dict[str, Any]:
        return {
            "status": ("online" if self.running else "stopped"),
            "services": sorted(self.services),
        }


def test_application_runtime_injects_cognitive_services():
    platform = build_aletheus_platform()

    runtime = ConstitutionalApplicationRuntime(platform=platform)

    application = CognitiveHostedApplication()

    application_id = application.manifest.application_id

    runtime.install(application)
    runtime.initialize(application_id)
    runtime.start(application_id)

    assert set(application.services) == {
        "cognition",
        "instrumentation",
        "scenarios",
    }

    assert application.running
