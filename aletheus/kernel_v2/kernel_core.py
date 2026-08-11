from __future__ import annotations

from typing import Any

from aletheus.kernel_v2.models import KernelEvent, KernelRegistryItem, KernelState


class AletheusAutonomousKernel:
    def __init__(self) -> None:
        self.version = "2.0.0-alpha"
        self.state = KernelState()
        self.events: list[KernelEvent] = []
        self.registry: list[KernelRegistryItem] = []

    def boot(self, runtime: Any) -> dict[str, Any]:
        health = runtime.commands.dispatch("runtime.health", {}).results.get(
            "health", {}
        )

        self.state.status = "online"
        self.state.services = health.get("services", 0)
        self.state.applications = health.get("applications", 0)
        self.state.missions = health.get("active_missions", 0)
        self.state.agents = health.get("online_agents", 0)

        self.publish(
            event_type="kernel.booted",
            source="kernel_v2",
            payload={"version": self.version, "runtime": health},
        )

        return self.status()

    def publish(
        self, event_type: str, source: str, payload: dict[str, Any] | None = None
    ) -> KernelEvent:
        event = KernelEvent(
            event_type=event_type,
            source=source,
            payload=payload or {},
        )
        self.events.append(event)
        self.state.events = len(self.events)
        return event

    def register(
        self,
        name: str,
        item_type: str,
        status: str = "registered",
        metadata: dict[str, Any] | None = None,
    ) -> KernelRegistryItem:
        existing = next(
            (
                item
                for item in self.registry
                if item.name == name and item.item_type == item_type
            ),
            None,
        )
        if existing:
            return existing

        item = KernelRegistryItem(
            name=name,
            item_type=item_type,
            status=status,
            metadata=metadata or {},
        )
        self.registry.append(item)

        self.publish(
            event_type="kernel.registry.item_registered",
            source="kernel_v2",
            payload=item.to_dict(),
        )

        return item

    def sync_runtime(self, runtime: Any) -> dict[str, Any]:
        diagnostics = runtime.commands.dispatch("runtime.diagnostics", {}).results
        health = runtime.commands.dispatch("runtime.health", {}).results.get(
            "health", {}
        )

        for service_name in diagnostics.get("diagnostics", {}).get("services", []):
            self.register(
                name=service_name,
                item_type="service",
                status="online",
                metadata={"source": "runtime.diagnostics"},
            )

        apps = runtime.commands.dispatch("application.list", {}).results.get(
            "applications", []
        )
        for app in apps:
            self.register(
                name=app.get("name", "Unnamed Application"),
                item_type="application",
                status=app.get("status", "registered"),
                metadata=app,
            )

        agents = runtime.commands.dispatch("agent.list", {}).results.get("agents", [])
        for agent in agents:
            self.register(
                name=agent.get("name", "Unnamed Agent"),
                item_type="agent",
                status=agent.get("status", "online"),
                metadata=agent,
            )

        self.state.services = health.get("services", 0)
        self.state.applications = health.get("applications", 0)
        self.state.missions = health.get("active_missions", 0)
        self.state.agents = health.get("online_agents", 0)

        self.publish(
            event_type="kernel.runtime.synced",
            source="kernel_v2",
            payload={"health": health, "registry_items": len(self.registry)},
        )

        return self.status()

    def route_event(
        self, event_type: str, source: str, payload: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        event = self.publish(
            event_type=event_type, source=source, payload=payload or {}
        )

        return {
            "event": event.to_dict(),
            "routed_to": [
                "memory",
                "learning",
                "optimization",
                "founder_workspace",
            ],
            "status": "routed",
        }

    def status(self) -> dict[str, Any]:
        return {
            "kernel": self.state.to_dict(),
            "registry_items": len(self.registry),
            "events": len(self.events),
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "status": self.status(),
            "registry": [item.to_dict() for item in self.registry],
            "events": [event.to_dict() for event in self.events[-50:]],
        }

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}

        for item in self.registry:
            by_type[item.item_type] = by_type.get(item.item_type, 0) + 1

        return {
            "version": self.version,
            "status": self.state.status,
            "events": len(self.events),
            "registry_items": len(self.registry),
            "registry_by_type": by_type,
        }


kernel_core = AletheusAutonomousKernel()
