import asyncio
import json

from aletheus.tooling.event_pipeline.engine import EventPipeline
from aletheus.tooling.event_pipeline.models import ConstitutionalEvent


def test_pipeline_publishes_and_subscribes(tmp_path) -> None:
    bus = tmp_path / "bus.json"
    bus.write_text(json.dumps({"channels": []}))
    pipeline = EventPipeline(bus, tmp_path / "out")
    received = []

    async def subscriber(event: ConstitutionalEvent) -> None:
        received.append(event.event_type)

    pipeline.subscribe("evidence.created", subscriber)
    asyncio.run(
        pipeline.publish(
            ConstitutionalEvent(
                event_type="evidence.created",
                authority="Evidence Engine",
                payload={},
            )
        )
    )
    assert received == ["evidence.created"]
