from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aletheus.runtime.context import RuntimeContext


@dataclass
class PipelineStep:
    name: str
    engine_name: str
    required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "engine_name": self.engine_name,
            "required": self.required,
        }


@dataclass
class Pipeline:
    name: str
    steps: list[PipelineStep] = field(default_factory=list)

    def add_step(self, name: str, engine_name: str, required: bool = True) -> None:
        self.steps.append(
            PipelineStep(name=name, engine_name=engine_name, required=required)
        )

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "steps": [step.to_dict() for step in self.steps]}


class PipelineExecutor:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime
        self.pipelines: dict[str, Pipeline] = {}

    def register(self, pipeline: Pipeline) -> None:
        self.pipelines[pipeline.name] = pipeline

    def execute(self, pipeline_name: str, context: RuntimeContext) -> RuntimeContext:
        if pipeline_name not in self.pipelines:
            context.add_error(f"Pipeline not registered: {pipeline_name}")
            return context
        pipeline = self.pipelines[pipeline_name]
        context.add_trace("pipeline.start", pipeline_name)
        for step in pipeline.steps:
            before_error_count = len(context.errors)
            context.add_trace("pipeline.step", step.to_dict())
            context = self.runtime.engines.run(step.engine_name, context)
            if step.required and len(context.errors) > before_error_count:
                context.add_trace("pipeline.halted", step.name)
                break
        context.add_trace("pipeline.finish", pipeline_name)
        return context

    def list(self) -> dict[str, Any]:
        return {name: pipeline.to_dict() for name, pipeline in self.pipelines.items()}
