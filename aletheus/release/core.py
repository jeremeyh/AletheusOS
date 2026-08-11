from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class ReleaseManifest:
    version: str = "1.0.0-genesis"
    codename: str = "Genesis"
    organization: str = "6th Dimension Multimedia"
    product: str = "Aletheus™"
    product_type: str = "Universal Intelligence Operating System"
    released_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    stable_subsystems: list[str] = field(
        default_factory=lambda: [
            "Runtime Core",
            "Memory Core",
            "Cognition Core",
            "Knowledge Graph Engine",
            "Autonomous Mission Engine",
            "Founder Workspace",
            "Native Application Manager",
            "Command Bus",
            "Event Bus",
            "Scheduler",
            "Workflow Engine",
            "Pipeline Engine",
            "Plugin Framework",
            "Diagnostics",
            "Metrics",
        ]
    )

    reference_applications: list[str] = field(
        default_factory=lambda: [
            "Card Hawk Foundation™",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "codename": self.codename,
            "organization": self.organization,
            "product": self.product,
            "product_type": self.product_type,
            "released_at": self.released_at,
            "stable_subsystems": self.stable_subsystems,
            "reference_applications": self.reference_applications,
        }


class AletheusReleaseCore:
    def __init__(self) -> None:
        self.manifest = ReleaseManifest()

    def status(self) -> dict[str, Any]:
        return self.manifest.to_dict()

    def validate_runtime(self, runtime: Any) -> dict[str, Any]:
        health = runtime.commands.dispatch("runtime.health").results.get("health", {})
        diagnostics = runtime.commands.dispatch("runtime.diagnostics").results

        required_services = [
            "Aletheus Runtime Core",
            "Aletheus Memory Core",
            "Aletheus Cognition Core",
            "Aletheus Knowledge Graph Engine",
            "Aletheus Autonomous Mission Engine",
            "Aletheus Founder Workspace",
            "Aletheus Native Application Manager",
        ]

        services = diagnostics.get("diagnostics", {}).get("services", [])
        missing = [service for service in required_services if service not in services]

        return {
            "release": self.status(),
            "runtime_health": health,
            "required_services": required_services,
            "missing_services": missing,
            "stable": health.get("status") == "online" and not missing,
        }


release_core = AletheusReleaseCore()
