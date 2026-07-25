"""
Automation Models

Genesis 13.42
"""

from dataclasses import dataclass, field


@dataclass
class WorkflowDefinition:


    workflow_id: str

    name: str

    trigger: str

    steps: list = field(
        default_factory=list
    )

    status: str = "created"

