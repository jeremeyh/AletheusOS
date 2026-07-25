from __future__ import annotations

from typing import Any

from aletheus.workflows_v2.models import WorkflowEvent, WorkflowExecution, WorkflowNode


class AletheusWorkflowFabric:
    def __init__(self) -> None:
        self.version = "2.0.0-d"
        self.workflows: list[WorkflowExecution] = []
        self.events: list[WorkflowEvent] = []

    def emit(self, workflow_id: str, event_type: str, message: str, payload: dict[str, Any] | None = None) -> WorkflowEvent:
        item = WorkflowEvent(
            workflow_id=workflow_id,
            event_type=event_type,
            message=message,
            payload=payload or {},
        )
        self.events.append(item)
        return item

    def default_nodes(self, objective: str, application: str) -> list[dict[str, Any]]:
        lower = objective.lower()

        if "card hawk" in lower or "marketplace" in lower or "asset" in lower:
            return [
                {
                    "title": "Build universal context",
                    "node_type": "command",
                    "command": "uil.context",
                    "payload": {"question": objective},
                    "assigned_agent": "Knowledge Agent",
                    "application": application,
                },
                {
                    "title": "Generate predictive forecast",
                    "node_type": "command",
                    "command": "predict.forecast",
                    "payload": {"horizon": "workflow execution"},
                    "assigned_agent": "Market Agent",
                    "application": application,
                },
                {
                    "title": "Create autonomous mission",
                    "node_type": "command",
                    "command": "mission.v2.create",
                    "payload": {
                        "title": "Workflow Generated Mission",
                        "objective": objective,
                        "application": application,
                        "priority": "high",
                    },
                    "assigned_agent": "Executive Agent",
                    "application": application,
                },
                {
                    "title": "Run multi-agent orchestration",
                    "node_type": "command",
                    "command": "agent.orchestrate",
                    "payload": {"objective": objective},
                    "assigned_agent": "Executive Agent",
                    "application": application,
                },
                {
                    "title": "Record learning experience",
                    "node_type": "command",
                    "command": "learn.record",
                    "payload": {
                        "event_type": "workflow_execution",
                        "description": f"Workflow executed objective: {objective}",
                        "source": "workflow_fabric",
                        "outcome": "completed",
                        "confidence": 0.86,
                    },
                    "assigned_agent": "Memory Agent",
                    "application": application,
                },
            ]

        return [
            {
                "title": "Reason over objective",
                "node_type": "command",
                "command": "uil.reason",
                "payload": {"question": objective},
                "assigned_agent": "Executive Agent",
                "application": application,
            },
            {
                "title": "Create plan",
                "node_type": "command",
                "command": "planning.create",
                "payload": {"objective": objective, "priority": "high"},
                "assigned_agent": "Executive Agent",
                "application": application,
            },
            {
                "title": "Record learning",
                "node_type": "command",
                "command": "learn.record",
                "payload": {
                    "event_type": "workflow_execution",
                    "description": f"Workflow executed objective: {objective}",
                    "source": "workflow_fabric",
                    "outcome": "completed",
                    "confidence": 0.82,
                },
                "assigned_agent": "Memory Agent",
                "application": application,
            },
        ]

    def create_workflow(
        self,
        title: str,
        objective: str,
        application: str = "AletheusOS",
        nodes: list[dict[str, Any]] | None = None,
    ) -> WorkflowExecution:
        workflow_nodes = [
            WorkflowNode(
                title=item.get("title", "Untitled Node"),
                node_type=item.get("node_type", "command"),
                command=item.get("command", ""),
                payload=item.get("payload", {}),
                assigned_agent=item.get("assigned_agent", "Executive Agent"),
                application=item.get("application", application),
            )
            for item in (nodes or self.default_nodes(objective, application))
        ]

        workflow = WorkflowExecution(
            title=title,
            objective=objective,
            application=application,
            status="queued",
            nodes=workflow_nodes,
        )
        self.workflows.append(workflow)
        self.emit(workflow.workflow_id, "workflow.created", f"Workflow created: {title}", workflow.to_dict())
        return workflow

    def get_workflow(self, workflow_id: str) -> WorkflowExecution | None:
        return next((item for item in self.workflows if item.workflow_id == workflow_id), None)

    def list_workflows(self, status: str | None = None) -> list[dict[str, Any]]:
        items = self.workflows
        if status:
            items = [workflow for workflow in items if workflow.status == status]
        return [workflow.to_dict() for workflow in items]

    def execute_node(self, workflow: WorkflowExecution, node: WorkflowNode, runtime: Any) -> dict[str, Any]:
        node.start()
        self.emit(workflow.workflow_id, "workflow.node.started", f"Node started: {node.title}", node.to_dict())

        if node.node_type == "command" and node.command:
            context = runtime.commands.dispatch(node.command, node.payload, application=node.application)
            result = {
                "command": node.command,
                "results": context.results,
                "errors": context.errors,
            }

            if context.errors:
                node.fail(result)
                self.emit(workflow.workflow_id, "workflow.node.failed", f"Node failed: {node.title}", node.to_dict())
            else:
                node.complete(result)
                self.emit(workflow.workflow_id, "workflow.node.completed", f"Node completed: {node.title}", node.to_dict())

            return result

        assignment = runtime.commands.dispatch(
            "agent.task.assign",
            {
                "agent_name": node.assigned_agent,
                "title": node.title,
                "payload": node.payload,
            },
        )
        agent_run = runtime.commands.dispatch("agent.run", {"agent_name": node.assigned_agent})

        result = {
            "assignment": assignment.results,
            "agent_run": agent_run.results,
            "errors": assignment.errors + agent_run.errors,
        }

        if result["errors"]:
            node.fail(result)
            self.emit(workflow.workflow_id, "workflow.node.failed", f"Node failed: {node.title}", node.to_dict())
        else:
            node.complete(result)
            self.emit(workflow.workflow_id, "workflow.node.completed", f"Node completed: {node.title}", node.to_dict())

        return result

    def execute_next(self, workflow_id: str, runtime: Any) -> dict[str, Any]:
        workflow = self.get_workflow(workflow_id)
        if workflow is None:
            return {"error": f"Workflow not found: {workflow_id}"}

        if workflow.status in {"queued", "created"}:
            workflow.start()
            self.emit(workflow.workflow_id, "workflow.started", f"Workflow started: {workflow.title}", workflow.to_dict())

        pending = [node for node in workflow.nodes if node.status == "queued"]
        if not pending:
            workflow.complete_if_ready()
            workflow.fail_if_needed()
            return {"workflow": workflow.to_dict(), "message": "No queued nodes."}

        node = pending[0]
        result = self.execute_node(workflow, node, runtime)

        workflow.complete_if_ready()
        workflow.fail_if_needed()

        if workflow.status == "completed":
            self.emit(workflow.workflow_id, "workflow.completed", f"Workflow completed: {workflow.title}", workflow.to_dict())
        elif workflow.status == "failed":
            self.emit(workflow.workflow_id, "workflow.failed", f"Workflow failed: {workflow.title}", workflow.to_dict())

        return {
            "workflow": workflow.to_dict(),
            "executed_node": node.to_dict(),
            "result": result,
        }

    def execute_workflow(self, workflow_id: str, runtime: Any) -> dict[str, Any]:
        outputs = []

        while True:
            workflow = self.get_workflow(workflow_id)
            if workflow is None:
                return {"error": f"Workflow not found: {workflow_id}"}

            if workflow.status in {"completed", "failed", "cancelled"}:
                break

            result = self.execute_next(workflow_id, runtime)
            outputs.append(result)

            workflow = self.get_workflow(workflow_id)
            if workflow is None or workflow.status in {"completed", "failed", "cancelled"}:
                break

        workflow = self.get_workflow(workflow_id)

        runtime.commands.dispatch(
            "learn.record",
            {
                "event_type": "workflow_execution",
                "description": f"Workflow completed: {workflow.title if workflow else workflow_id}",
                "source": "workflow_fabric",
                "outcome": workflow.status if workflow else "unknown",
                "confidence": 0.88,
                "metadata": workflow.to_dict() if workflow else {},
            },
        )

        return {
            "workflow": workflow.to_dict() if workflow else None,
            "outputs": outputs,
        }

    def pause(self, workflow_id: str) -> dict[str, Any]:
        workflow = self.get_workflow(workflow_id)
        if workflow is None:
            return {"error": f"Workflow not found: {workflow_id}"}
        workflow.status = "paused"
        self.emit(workflow_id, "workflow.paused", f"Workflow paused: {workflow.title}", workflow.to_dict())
        return workflow.to_dict()

    def resume(self, workflow_id: str) -> dict[str, Any]:
        workflow = self.get_workflow(workflow_id)
        if workflow is None:
            return {"error": f"Workflow not found: {workflow_id}"}
        workflow.status = "queued"
        self.emit(workflow_id, "workflow.resumed", f"Workflow resumed: {workflow.title}", workflow.to_dict())
        return workflow.to_dict()

    def cancel(self, workflow_id: str) -> dict[str, Any]:
        workflow = self.get_workflow(workflow_id)
        if workflow is None:
            return {"error": f"Workflow not found: {workflow_id}"}
        workflow.status = "cancelled"
        self.emit(workflow_id, "workflow.cancelled", f"Workflow cancelled: {workflow.title}", workflow.to_dict())
        return workflow.to_dict()

    def history(self, workflow_id: str = "") -> list[dict[str, Any]]:
        events = self.events
        if workflow_id:
            events = [event for event in events if event.workflow_id == workflow_id]
        return [event.to_dict() for event in events]

    def stats(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "workflows": len(self.workflows),
            "queued": len([item for item in self.workflows if item.status == "queued"]),
            "running": len([item for item in self.workflows if item.status == "running"]),
            "completed": len([item for item in self.workflows if item.status == "completed"]),
            "failed": len([item for item in self.workflows if item.status == "failed"]),
            "paused": len([item for item in self.workflows if item.status == "paused"]),
            "cancelled": len([item for item in self.workflows if item.status == "cancelled"]),
            "events": len(self.events),
        }


workflow_v2_core = AletheusWorkflowFabric()
