from __future__ import annotations

from collections.abc import Callable
from typing import Any

from aletheus.runtime import Pipeline, WorkflowGraph, runtime_core


class AletheusRuntimeSDK:
    def register_engine(self, name: str, handler: Callable[..., Any]) -> None:
        runtime_core.register_engine(name, handler)

    def register_service(self, name: str, service: Any) -> None:
        runtime_core.register_service(name, service)

    def register_pipeline(self, pipeline: Pipeline) -> None:
        runtime_core.register_pipeline(pipeline)

    def register_workflow(self, workflow: WorkflowGraph) -> None:
        runtime_core.register_workflow(workflow)

    def dispatch(
        self, command: str, payload: dict | None = None, application: str = "system"
    ) -> dict:
        return runtime_core.commands.dispatch(
            command, payload or {}, application=application
        ).to_dict()


sdk = AletheusRuntimeSDK()
