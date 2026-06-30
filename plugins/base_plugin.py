from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

from services.context import PipelineContext


class BasePlugin(ABC):
    name = "BasePlugin"
    version = "1.0.0"
    description = "CardHawkOS plugin base class."
    enabled = True

    def initialize(self) -> Dict[str, Any]:
        return {"plugin": self.name, "status": "initialized", "version": self.version}

    @abstractmethod
    def execute(self, context: PipelineContext) -> PipelineContext:
        raise NotImplementedError

    def shutdown(self) -> Dict[str, Any]:
        return {"plugin": self.name, "status": "shutdown"}

    def manifest(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "enabled": self.enabled,
        }
