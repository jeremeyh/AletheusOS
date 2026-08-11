"""
CardHawk OS™
Runtime Snapshot
"""

from datetime import datetime

from core.engine_registry import engine_registry
from core.event_bus import event_bus
from core.service_registry import service_registry
from intelligence.projections.manager import projection_manager
from kernel.runtime import kernel


def snapshot():

    kernel.boot()

    return {
        "generated": datetime.utcnow().isoformat(),
        "engines": list(engine_registry.all().keys()),
        "services": list(service_registry.services.keys()),
        "projections": projection_manager.list(),
        "listeners": event_bus.listeners(),
    }
