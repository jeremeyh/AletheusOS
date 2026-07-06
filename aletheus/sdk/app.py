from __future__ import annotations

from .capabilities import CapabilityClient
from .engines import EngineClient
from .events import EventClient
from .services import ServiceClient


class AletheusApp:
    GENESIS = "21.4"
    VERSION = "0.1.0"

    def __init__(self, name: str, overlay: str | None = None):
        self.name = name
        self.overlay = overlay

        self.engines = EngineClient(app=self)
        self.capabilities = CapabilityClient(app=self)
        self.events = EventClient(app=self)
        self.services = ServiceClient(app=self)

    def engine(self, engine_id_or_name: str):
        return self.engines.get(engine_id_or_name)

    def capability(self, capability_id: str):
        return self.capabilities.has(capability_id)

    def on(self, event_type: str):
        return self.events.on(event_type)

    def emit(self, event_type: str, payload: dict | None = None):
        return self.events.emit(event_type, payload or {})

    def ledger(self):
        return self.services.ledger()

    def memory(self):
        return self.services.memory()

    def graph(self):
        return self.services.graph()

    def reason(self):
        return self.services.reason()

    def simulate(self):
        return self.services.simulate()

    def digital_twin(self):
        return self.services.digital_twin()

    def health(self):
        return {
            "name": self.name,
            "overlay": self.overlay,
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "online",
        }
