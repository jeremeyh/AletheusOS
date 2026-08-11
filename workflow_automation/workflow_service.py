import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class WorkflowStep:
    name: str
    status: str = "pending"
    notes: str = ""


@dataclass
class WorkflowRun:
    workflow_type: str
    subject: str = ""
    status: str = "draft"
    steps: list = field(default_factory=list)
    run_id: str = field(default_factory=lambda: f"WF-{uuid.uuid4().hex[:10].upper()}")
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class WorkflowAutomationService:
    """CardHawk OS™ 6.0A Workflow Automation™."""

    TEMPLATES = {
        "Asset Intake Wizard™": [
            "Upload Images",
            "Run Hawk A•Eye™",
            "Review Asset DNA™",
            "Compute THORᵡ™",
            "Founder Approval",
            "Save to Asset Vault™",
        ],
        "Acquisition Workflow™": [
            "Import Listing",
            "Normalize Marketplace Data",
            "Compute THORᵡ™",
            "Run Acquisition AI™",
            "Generate Offer Strategy",
            "Add Watchlist / Purchase",
        ],
        "Exit Workflow™": [
            "Recompute Market Value",
            "Run Exit Intelligence™",
            "Grade Recommendation",
            "Suggested Marketplace",
            "Expected Proceeds",
            "Archive Sale",
        ],
    }

    _runs = []

    @classmethod
    def start(cls, workflow_type, subject=""):
        steps = [WorkflowStep(name=s) for s in cls.TEMPLATES.get(workflow_type, [])]
        run = WorkflowRun(
            workflow_type=workflow_type, subject=subject, steps=steps, status="active"
        )
        cls._runs.append(run)
        return run

    @classmethod
    def advance(cls, run_id):
        for run in cls._runs:
            if run.run_id == run_id:
                for step in run.steps:
                    if step.status == "pending":
                        step.status = "complete"
                        break
                if all(s.status == "complete" for s in run.steps):
                    run.status = "complete"
                return run
        return None

    @classmethod
    def all(cls):
        return cls._runs
