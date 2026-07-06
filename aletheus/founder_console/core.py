from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any


@dataclass
class FounderConsoleComponent:
    name: str
    status: str
    version: str = "unknown"
    details: dict[str, Any] | None = None


class FounderConsoleBackend:
    """
    Founder Console Backend™

    Aggregates health, status, version, and statistics from AletheusOS
    subsystems into one operating report.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.generated_at = datetime.utcnow().isoformat()

    def collect(self) -> dict[str, Any]:
        components = []

        components.append(self._runtime())
        components.append(self._executive_kernel())
        components.append(self._platform_layer())

        return {
            "founder_console": {
                "name": "Founder Console Backend",
                "version": self.VERSION,
                "generated_at": self.generated_at,
                "status": self._overall_status(components),
                "components": [asdict(component) for component in components],
            }
        }

    def _overall_status(self, components: list[FounderConsoleComponent]) -> str:
        statuses = {component.status for component in components}

        if "critical" in statuses or "failed" in statuses:
            return "critical"

        if "degraded" in statuses or "warning" in statuses:
            return "degraded"

        return "healthy"

    def _runtime(self) -> FounderConsoleComponent:
        try:
            from aletheus.runtime import runtime_core

            runtime_core.boot()

            details = {
                "status": getattr(runtime_core, "status", "unknown"),
                "version": getattr(runtime_core, "version", "unknown"),
            }

            if hasattr(runtime_core, "commands"):
                try:
                    details["commands"] = runtime_core.commands.count()
                except Exception:
                    details["commands"] = "unknown"

            if hasattr(runtime_core, "services"):
                try:
                    details["services"] = runtime_core.services.count()
                except Exception:
                    details["services"] = "unknown"

            return FounderConsoleComponent(
                name="Runtime",
                status=details.get("status", "unknown"),
                version=str(details.get("version", "unknown")),
                details=details,
            )

        except Exception as exc:
            return FounderConsoleComponent(
                name="Runtime",
                status="failed",
                details={"error": f"{type(exc).__name__}: {exc}"},
            )

    def _executive_kernel(self) -> FounderConsoleComponent:
        try:
            from aletheus.executive_kernel import executive_kernel

            health = executive_kernel.health()

            return FounderConsoleComponent(
                name="Executive Kernel",
                status=health.get("status", "unknown"),
                version=health.get("version", "unknown"),
                details=health,
            )

        except Exception as exc:
            return FounderConsoleComponent(
                name="Executive Kernel",
                status="failed",
                details={"error": f"{type(exc).__name__}: {exc}"},
            )

    def _platform_layer(self) -> FounderConsoleComponent:
        try:
            from aletheus.platform.platform_layer import PlatformLayer

            report = PlatformLayer().inspect()
            platform = report.get("platform", {})

            return FounderConsoleComponent(
                name="Platform Layer",
                status=platform.get("status", "unknown"),
                version=platform.get("version", "unknown"),
                details={
                    "score": platform.get("score"),
                    "findings": platform.get("findings", []),
                },
            )

        except Exception as exc:
            return FounderConsoleComponent(
                name="Platform Layer",
                status="failed",
                details={"error": f"{type(exc).__name__}: {exc}"},
            )


founder_console_backend = FounderConsoleBackend()
