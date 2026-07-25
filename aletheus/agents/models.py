"""
Aletheus Agent Models

Genesis 13.27
Extended Genesis 81 Agent Foundation
"""

from dataclasses import dataclass, field


@dataclass
class AgentCapability:
    """
    Defines a capability available to an Aletheus agent.
    """

    name: str

    description: str = ""

    domain: str = ""



    def describe(self):

        return {

            "capability":
            self.name,

            "description":
            self.description,

            "domain":
            self.domain

        }



@dataclass
class AgentTask:
    """
    Represents a task assigned to an Aletheus agent.
    """

    task_id: str

    objective: str

    context: dict = field(
        default_factory=dict
    )

    status: str = "created"



@dataclass
class AletheusAgent:
    """
    Core Aletheus autonomous agent model.
    """

    agent_id: str

    name: str

    purpose: str

    capabilities: list = field(
        default_factory=list
    )

    status: str = "created"



    def add_capability(
        self,
        capability
    ):

        self.capabilities.append(
            capability
        )



    def describe(self):

        return {

            "agent_id":
            self.agent_id,

            "name":
            self.name,

            "purpose":
            self.purpose,

            "capabilities":
            len(self.capabilities),

            "status":
            self.status

        }



@dataclass
class AgentDefinition:
    """
    Legacy compatibility model.
    """

    agent_id: str

    name: str

    purpose: str

    capabilities: list = field(
        default_factory=list
    )

    status: str = "created"



@dataclass
class AgentMission:
    """
    Agent mission definition.
    """

    mission_id: str

    objective: str

    constraints: dict = field(
        default_factory=dict
    )

