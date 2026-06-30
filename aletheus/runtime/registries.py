from __future__ import annotations
from typing import Any, Callable, Dict, List
from aletheus.runtime.context import RuntimeContext

class EngineRegistry:
    def __init__(self) -> None: self.engines: Dict[str, Callable[[RuntimeContext], RuntimeContext]] = {}
    def register(self, name: str, handler: Callable[[RuntimeContext], RuntimeContext]) -> None: self.engines[name] = handler
    def run(self, name: str, context: RuntimeContext) -> RuntimeContext:
        if name not in self.engines:
            context.add_error(f"Engine not registered: {name}"); return context
        context.add_trace('engine.start', name)
        result = self.engines[name](context)
        result.add_trace('engine.finish', name)
        return result
    def list(self) -> List[str]: return sorted(self.engines.keys())
    def count(self) -> int: return len(self.engines)

class ServiceRegistry:
    def __init__(self) -> None: self.services: Dict[str, Any] = {}
    def register(self, name: str, service: Any) -> None: self.services[name] = service
    def get(self, name: str, default: Any = None) -> Any: return self.services.get(name, default)
    def list(self) -> List[str]: return sorted(self.services.keys())
    def count(self) -> int: return len(self.services)
