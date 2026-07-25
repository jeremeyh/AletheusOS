"""
CardHawk OS™
Platform Kernel
"""

from core.bootstrap import bootstrap
from core.engine_registry import engine_registry
from core.event_bus import event_bus
from core.service_registry import service_registry
from intelligence.projections.manager import projection_manager


class Kernel:

    def __init__(self):

        self.booted = False

    def boot(self):

        if self.booted:
            return

        bootstrap.boot()

        self.booted = True

    def status(self):

        return {

            "engines": len(engine_registry.all()),

            "services": len(service_registry.services),

            "projections": len(projection_manager.projections),

            "listeners": event_bus.listeners()

        }


kernel = Kernel()
