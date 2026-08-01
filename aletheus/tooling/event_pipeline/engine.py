from __future__ import annotations

import asyncio
import json
from collections import defaultdict
from collections.abc import Awaitable, Callable
from pathlib import Path
from typing import Any

from .models import ConstitutionalEvent

Subscriber = Callable[[ConstitutionalEvent], Awaitable[None]]


class EventPipeline:
    def __init__(self, service_bus: Path, output: Path) -> None:
        self.service_bus = service_bus
        self.output = output
        self._subscribers: dict[str, list[Subscriber]] = defaultdict(list)
        self._history: list[dict[str, Any]] = []

    def subscribe(self, event_type: str, subscriber: Subscriber) -> None:
        self._subscribers[event_type].append(subscriber)

    async def publish(self, event: ConstitutionalEvent) -> None:
        subscribers = [
            *self._subscribers.get(event.event_type, []),
            *self._subscribers.get("*", []),
        ]
        await asyncio.gather(
            *(subscriber(event) for subscriber in subscribers),
            return_exceptions=False,
        )
        self._history.append(event.to_dict())

    async def run_default_flow(self) -> dict[str, Any]:
        bus = json.loads(self.service_bus.read_text(encoding="utf-8"))
        channel_count = len(bus.get("channels", []))
        event_types = [
            "evidence.created",
            "knowledge.resolved",
            "reasoning.completed",
            "planning.completed",
            "execution.completed",
        ]
        received: list[str] = []

        async def recorder(event: ConstitutionalEvent) -> None:
            received.append(event.event_type)

        self.subscribe("*", recorder)
        for event_type in event_types:
            await self.publish(
                ConstitutionalEvent(
                    event_type=event_type,
                    authority="Constitutional Event Pipeline",
                    payload={"channel_count": channel_count},
                )
            )

        report = {
            "events": self._history,
            "event_count": len(self._history),
            "received": received,
            "service_bus_channels": channel_count,
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "constitutional-event-pipeline.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
