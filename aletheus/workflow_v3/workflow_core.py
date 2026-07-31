from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from aletheus.time_utils import utc_now, utc_now_iso


def utc_now() -> str:
    return utc_now_iso()


@dataclass
class WorkflowStep:
    title: str
    agent: str
    status: str = "pending"


@dataclass
class Workflow:
    title: str
    description: str

    workflow_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    status: str = "created"

    created_at: str = field(default_factory=utc_now)
    started_at: str | None = None
    completed_at: str | None = None

    checkpoint: int = 0

    steps: list[WorkflowStep] = field(default_factory=list)

    def start(self):
        self.status = "running"
        self.started_at = utc_now()

    def pause(self):
        self.status = "paused"

    def resume(self):
        self.status = "running"

    def cancel(self):
        self.status = "cancelled"

    def complete(self):
        self.status = "completed"
        self.completed_at = utc_now()

    def to_dict(self):
        return {
            "workflow_id": self.workflow_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "checkpoint": self.checkpoint,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "steps": [
                {
                    "title": s.title,
                    "agent": s.agent,
                    "status": s.status,
                }
                for s in self.steps
            ],
        }


class AletheusWorkflowEngine:
    VERSION = "2.8.0"

    def __init__(self):

        self.workflows: dict[str, Workflow] = {}

    def bootstrap(self):

        if self.workflows:
            return self.statistics()

        workflow = Workflow(
            title="Card Hawk Acquisition Workflow",
            description="Research → Marketplace → Portfolio → Decision",
        )

        workflow.steps.extend(
            [
                WorkflowStep("Research Player", "Research Agent"),
                WorkflowStep("Marketplace Comps", "Marketplace Agent"),
                WorkflowStep("Portfolio Analysis", "Portfolio Agent"),
                WorkflowStep("Decision Engine", "Founder Agent"),
            ]
        )

        self.workflows[workflow.workflow_id] = workflow

        return self.statistics()

    def create(self, title, description):

        workflow = Workflow(title=title, description=description)

        self.workflows[workflow.workflow_id] = workflow

        return workflow.to_dict()

    def start(self, workflow_id):

        workflow = self.workflows[workflow_id]

        workflow.start()

        return workflow.to_dict()

    def pause(self, workflow_id):

        workflow = self.workflows[workflow_id]

        workflow.pause()

        return workflow.to_dict()

    def resume(self, workflow_id):

        workflow = self.workflows[workflow_id]

        workflow.resume()

        return workflow.to_dict()

    def cancel(self, workflow_id):

        workflow = self.workflows[workflow_id]

        workflow.cancel()

        return workflow.to_dict()

    def status(self):

        return {"workflows": [w.to_dict() for w in self.workflows.values()]}

    def statistics(self):

        return {
            "version": self.VERSION,
            "workflows": len(self.workflows),
            "running": sum(w.status == "running" for w in self.workflows.values()),
            "paused": sum(w.status == "paused" for w in self.workflows.values()),
            "completed": sum(w.status == "completed" for w in self.workflows.values()),
        }


workflow_core = AletheusWorkflowEngine()
