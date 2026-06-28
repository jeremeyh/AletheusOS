"""
CardHawk OS™
Legacy Engine Adapter
"""

from core.engine_base import EngineBase


class EngineAdapter(EngineBase):

    def __init__(self, module):

        self.module = module

        self.name = getattr(module, "ENGINE_NAME", module.__name__.split(".")[-1])

        self.version = getattr(module, "ENGINE_VERSION", "legacy")

    def initialize(self):

        init = getattr(self.module, "initialize", None)

        if callable(init):
            init()

        return True

    def execute(self, payload):

        for fn in (
            "execute",
            "run",
            "process",
            "analyze",
            "evaluate",
            "predict",
        ):

            func = getattr(self.module, fn, None)

            if callable(func):
                return func(payload)

        print(f"{self.name}: no executable entry point found")

    def subscribe(self, event_bus):

        events = getattr(self.module, "EVENTS", [])

        handler = getattr(self.module, "handle_event", None)

        if callable(handler):

            for event in events:
                event_bus.subscribe(event, handler)

    def shutdown(self):

        fn = getattr(self.module, "shutdown", None)

        if callable(fn):
            fn()

        return True
