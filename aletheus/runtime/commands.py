from __future__ import annotations
from typing import Any, Callable, Dict, Optional
import time, traceback
from aletheus.runtime.context import RuntimeContext

class CommandBus:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime
        self.commands: Dict[str, Callable[[RuntimeContext], RuntimeContext]] = {}
    def register(self, command: str, handler: Callable[[RuntimeContext], RuntimeContext]) -> None: self.commands[command] = handler
    def dispatch(self, command: str, payload: Optional[Dict[str, Any]] = None, application: str = 'system') -> RuntimeContext:
        context = RuntimeContext(command=command, payload=payload or {}, application=application)
        started = time.time()
        try:
            if command not in self.commands:
                context.add_error(f"Command not registered: {command}"); return context
            context.add_trace('command.start', command)
            context = self.commands[command](context)
            context.add_trace('command.finish', command)
        except Exception as exc:
            context.add_error(str(exc)); context.add_error(traceback.format_exc())
        finally:
            elapsed = round(time.time() - started, 5)
            self.runtime.metrics.record('command.last', command)
            self.runtime.metrics.record('command.last_seconds', elapsed)
            self.runtime.events.publish('runtime.command.dispatched', {'command': command, 'application': application, 'elapsed_seconds': elapsed, 'errors': context.errors}, source='command_bus')
        return context
    def list(self) -> list[str]: return sorted(self.commands.keys())
    def count(self) -> int: return len(self.commands)
