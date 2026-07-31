from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from services.context import PipelineContext
from services.runtime_events import RuntimeEvent


class CommandBus:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime
        self.handlers: dict[str, Callable[[PipelineContext], PipelineContext]] = {}

    def register(
        self, command: str, handler: Callable[[PipelineContext], PipelineContext]
    ) -> None:
        self.handlers[command] = handler

    def dispatch(
        self, command: str, payload: dict[str, Any] | None = None
    ) -> PipelineContext:
        started = time.time()
        context = PipelineContext(command=command, payload=payload or {})
        try:
            handler = self.handlers.get(command)
            if not handler:
                context.add_error(f"Command not registered: {command}")
                return context
            context = handler(context)
            return context
        except Exception as exc:
            context.add_error(str(exc))
            return context
        finally:
            elapsed = round(time.time() - started, 4)
            self.runtime.metrics.record(
                "command.elapsed_seconds", elapsed, command=command
            )
            self.runtime.events.append(
                RuntimeEvent(
                    "command.dispatch",
                    {"command": command, "elapsed_seconds": elapsed, "ok": context.ok},
                    request_id=context.request_id,
                )
            )
