from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ManagedSubsystem:
    name: str
    instance: Any
    priority: int = 100
    metadata: dict[str, Any] = field(default_factory=dict)


class AletheumOrchestrator:
    """
    Aletheum Orchestrator™

    Coordinates the lifecycle of every major subsystem.

    Responsibilities

    • registration
    • boot ordering
    • shutdown ordering
    • health collection
    • verification
    • future dependency resolution

    The Orchestrator never contains business logic.
    It coordinates platform components.
    """

    VERSION = "0.1.0"

    def __init__(self):
        self._subsystems: list[ManagedSubsystem] = []

    def register(
        self,
        name: str,
        instance: Any,
        priority: int = 100,
        metadata: dict[str, Any] | None = None,
    ):
        self._subsystems.append(
            ManagedSubsystem(
                name=name,
                instance=instance,
                priority=priority,
                metadata=metadata or {},
            )
        )

        self._subsystems.sort(key=lambda s: s.priority)

    def registered(self):
        return [s.name for s in self._subsystems]

    def boot(self):
        results = []

        for subsystem in self._subsystems:
            status = "ready"

            if hasattr(subsystem.instance, "boot"):
                try:
                    subsystem.instance.boot()
                    status = "booted"
                except Exception as exc:
                    status = f"error: {exc}"

            results.append(
                {
                    "name": subsystem.name,
                    "status": status,
                }
            )

        return results

    def health(self):
        report = {}

        for subsystem in self._subsystems:
            if hasattr(subsystem.instance, "health"):
                try:
                    report[subsystem.name] = subsystem.instance.health()
                except Exception as exc:
                    report[subsystem.name] = {
                        "status": "error",
                        "error": str(exc),
                    }
            else:
                report[subsystem.name] = {
                    "status": "unknown",
                }

        return report

    def statistics(self):
        return {
            "version": self.VERSION,
            "registered_subsystems": len(self._subsystems),
            "subsystems": self.registered(),
        }


orchestrator = AletheumOrchestrator()
