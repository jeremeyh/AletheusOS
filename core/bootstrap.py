"""
CardHawk OS™
Platform Bootstrap
"""

from core.container import container
from core.discovery import discovery
from core.engine_registry import engine_registry
from core.event_bus import event_bus
from core.service_discovery import service_discovery


class Bootstrap:
    def __init__(self):
        self.initialized = False

    def boot(self):

        if self.initialized:
            return container

        print("=" * 60)
        print("CardHawk OS™ Boot Sequence")
        print("=" * 60)

        # ---------------------------------------------------
        # Discover Engines
        # ---------------------------------------------------

        engine_modules, engine_names = discovery.discover_package("engines")

        print(f"Discovered Engine Modules : {len(engine_modules)}")
        print(f"Registered Engines        : {len(engine_names)}")

        # ---------------------------------------------------
        # Discover Services
        # ---------------------------------------------------

        service_modules, service_names = service_discovery.discover("services")

        print(f"Registered Services       : {len(service_names)}")

        # ---------------------------------------------------
        # Initialize Engines
        # ---------------------------------------------------

        for engine in engine_registry.all().values():
            try:
                engine.initialize()
            except Exception as exc:
                print(f"[INIT] {engine.name}: {exc}")

        # ---------------------------------------------------
        # Subscribe Engines
        # ---------------------------------------------------

        for engine in engine_registry.all().values():
            try:
                engine.subscribe(event_bus)
            except Exception as exc:
                print(f"[SUBSCRIBE] {engine.name}: {exc}")

        self.initialized = True

        print("=" * 60)
        print("CardHawk OS™ READY")
        print("=" * 60)

        return container


bootstrap = Bootstrap()
