from __future__ import annotations

import time
import traceback
from collections.abc import Callable
from typing import Any

from aletheus.runtime.context import RuntimeContext


class CommandBus:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime
        self.commands: dict[str, Callable[[RuntimeContext], RuntimeContext]] = {}

    def register(
        self, command: str, handler: Callable[[RuntimeContext], RuntimeContext]
    ) -> None:
        self.commands[command] = handler

    def dispatch(
        self,
        command: str,
        payload: dict[str, Any] | None = None,
        application: str = "system",
    ) -> RuntimeContext:
        context = RuntimeContext(
            command=command, payload=payload or {}, application=application
        )
        started = time.time()
        try:
            if command not in self.commands:
                context.add_error(f"Command not registered: {command}")
                return context
            context.add_trace("command.start", command)
            context = self.commands[command](context)
            context.add_trace("command.finish", command)
        except Exception as exc:
            context.add_error(str(exc))
            context.add_error(traceback.format_exc())
        finally:
            elapsed = round(time.time() - started, 5)
            self.runtime.metrics.record("command.last", command)
            self.runtime.metrics.record("command.last_seconds", elapsed)
            self.runtime.events.publish(
                "runtime.command.dispatched",
                {
                    "command": command,
                    "application": application,
                    "elapsed_seconds": elapsed,
                    "errors": context.errors,
                },
                source="command_bus",
            )
        return context

    def list(self) -> list[str]:
        return sorted(self.commands.keys())

    def count(self) -> int:
        return len(self.commands)
