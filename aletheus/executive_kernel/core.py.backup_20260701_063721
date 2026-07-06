from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class CapabilityProvider:
    name: str
    capability: str
    handler: Callable[[dict[str, Any]], Any]
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityRequest:
    capability: str
    payload: dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityResult:
    capability: str
    provider: str | None
    status: str
    result: Any = None
    error: str | None = None


class ExecutiveKernel:
    """
    Executive Kernel™

    Capability-first orchestration layer for AletheusOS.

    Applications request capabilities.
    The kernel selects the correct provider.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self.providers: dict[str, list[CapabilityProvider]] = {}

    def register_provider(
        self,
        name: str,
        capability: str,
        handler: Callable[[dict[str, Any]], Any],
        priority: int = 100,
        metadata: dict[str, Any] | None = None,
    ) -> CapabilityProvider:
        provider = CapabilityProvider(
            name=name,
            capability=capability,
            handler=handler,
            priority=priority,
            metadata=metadata or {},
        )

        self.providers.setdefault(capability, []).append(provider)
        self.providers[capability].sort(key=lambda item: item.priority)

        return provider

    def capabilities(self) -> list[str]:
        return sorted(self.providers.keys())

    def providers_for(self, capability: str) -> list[CapabilityProvider]:
        return list(self.providers.get(capability, []))

    def request(
        self,
        capability: str,
        payload: dict[str, Any] | None = None,
    ) -> CapabilityResult:
        payload = payload or {}
        providers = self.providers_for(capability)

        if not providers:
            return CapabilityResult(
                capability=capability,
                provider=None,
                status="unavailable",
                error=f"No provider registered for capability: {capability}",
            )

        provider = providers[0]

        try:
            result = provider.handler(payload)
            return CapabilityResult(
                capability=capability,
                provider=provider.name,
                status="success",
                result=result,
            )
        except Exception as exc:
            return CapabilityResult(
                capability=capability,
                provider=provider.name,
                status="error",
                error=f"{type(exc).__name__}: {exc}",
            )

    def health(self) -> dict[str, Any]:
        return {
            "name": "Executive Kernel",
            "version": self.VERSION,
            "status": "online",
            "capabilities": len(self.providers),
            "providers": sum(len(v) for v in self.providers.values()),
        }


executive_kernel = ExecutiveKernel()
