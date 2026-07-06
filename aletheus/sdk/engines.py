from __future__ import annotations

from aletheus.overlay_manager import overlay_manager
from aletheus.runtime_intelligence import runtime_intelligence_core


class EngineHandle:
    def __init__(self, engine: dict):
        self.engine = engine

    def to_dict(self):
        return self.engine

    def health(self):
        metadata = self.engine.get("metadata", {})

        return {
            "engine_id": self.engine["engine_id"],
            "name": metadata.get("name", self.engine["engine_id"]),
            "status": self.engine["status"],
        }


class EngineClient:
    def __init__(self, app):
        self.app = app

    def all(self):
        runtime_intelligence_core.initialize()
        return runtime_intelligence_core.engines()

    def get(self, engine_id_or_name: str):
        runtime_intelligence_core.initialize()

        if self.app.overlay:
            overlay_manager.bootstrap_cardhawk()
            engine_id_or_name = overlay_manager.resolve(
                self.app.overlay,
                engine_id_or_name,
            )

        for engine in runtime_intelligence_core.engines():
            if engine["engine_id"] == engine_id_or_name:
                return EngineHandle(engine)

        raise KeyError(f"Engine not found: {engine_id_or_name}")
