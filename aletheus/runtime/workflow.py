from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from aletheus.runtime.context import RuntimeContext


@dataclass
class WorkflowNode:
    node_id: str
    command: str
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "node_id": self.node_id,
            "command": self.command,
            "payload": self.payload,
        }


@dataclass
class WorkflowGraph:
    name: str
    nodes: list[WorkflowNode] = field(default_factory=list)

    def add_node(
        self, node_id: str, command: str, payload: dict[str, Any] | None = None
    ) -> None:
        self.nodes.append(
            WorkflowNode(node_id=node_id, command=command, payload=payload or {})
        )

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "nodes": [node.to_dict() for node in self.nodes]}


class WorkflowExecutor:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime
        self.workflows: dict[str, WorkflowGraph] = {}

    def register(self, workflow: WorkflowGraph) -> None:
        self.workflows[workflow.name] = workflow

    def execute(
        self, workflow_name: str, application: str = "system"
    ) -> RuntimeContext:
        context = RuntimeContext(
            command=f"workflow.{workflow_name}", application=application
        )
        if workflow_name not in self.workflows:
            context.add_error(f"Workflow not registered: {workflow_name}")
            return context
        workflow = self.workflows[workflow_name]
        context.add_trace("workflow.start", workflow_name)
        node_results = {}
        for node in workflow.nodes:
            result = self.runtime.commands.dispatch(
                node.command, node.payload, application=application
            )
            node_results[node.node_id] = result.to_dict()
            if result.errors:
                context.errors.extend(result.errors)
        context.add_result("workflow", {"name": workflow_name, "nodes": node_results})
        context.add_trace("workflow.finish", workflow_name)
        return context

    def list(self) -> dict[str, Any]:
        return {name: workflow.to_dict() for name, workflow in self.workflows.items()}
