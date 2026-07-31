"""
Timeline Subscriber
"""

from core.event_bus import event_bus
from timeline.engine.projection import projection

EVENTS = [
    "asset.created",
    "dna.completed",
    "thorx.completed",
    "portfolio.updated",
    "founder.updated",
    "live_data.updated",
    "scout.completed",
]


def handle(payload, event_name):
    projection.project(event_name, payload)


for event_name in EVENTS:
    event_bus.subscribe(event_name, lambda payload, e=event_name: handle(payload, e))
