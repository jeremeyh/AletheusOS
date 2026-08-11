from __future__ import annotations

from typing import Any

from aletheus.runtime.context import RuntimeContext


class RuntimePlugin:
    name = "RuntimePlugin"
    version = "0.0.0"
    description = "Base runtime plugin."

    def initialize(self, runtime: Any) -> None:
        self.runtime = runtime

    def execute(self, context: RuntimeContext) -> RuntimeContext:
        context.add_result(self.name, {"status": "executed"})
        return context

    def shutdown(self) -> None:
        return None
