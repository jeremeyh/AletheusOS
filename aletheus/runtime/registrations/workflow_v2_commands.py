"""
Aletheus v2 Autonomous Workflow Command Registration.

Binds workflow.v2 commands directly to the bounded
AletheusWorkflowFabric.
"""

from __future__ import annotations

from typing import Any


def _serialize(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_workflow_v2_commands(runtime):
    commands = runtime.commands
    engine = runtime.workflow_v2

    def create(payload=None):
        payload = payload or {}

        workflow = engine.create_workflow(
            title=payload.get("title", "Untitled Workflow"),
            objective=payload.get("objective", ""),
            application=payload.get(
                "application",
                "AletheusOS",
            ),
            nodes=payload.get("nodes"),
        )

        return _serialize(workflow)

    def execute(payload=None):
        payload = payload or {}

        return engine.execute_workflow(
            workflow_id=payload.get("workflow_id", ""),
            runtime=runtime,
        )

    def execute_next(payload=None):
        payload = payload or {}

        return engine.execute_next(
            workflow_id=payload.get("workflow_id", ""),
            runtime=runtime,
        )

    def history(payload=None):
        payload = payload or {}

        return engine.history(
            workflow_id=payload.get("workflow_id", ""),
        )

    def statistics(payload=None):
        return engine.stats()

    commands.register(
        "workflow.v2.create",
        create,
        replace=True,
    )

    commands.register(
        "workflow.v2.execute",
        execute,
        replace=True,
    )

    commands.register(
        "workflow.v2.execute_next",
        execute_next,
        replace=True,
    )

    commands.register(
        "workflow.v2.history",
        history,
        replace=True,
    )

    commands.register(
        "workflow.v2.stats",
        statistics,
        replace=True,
    )
