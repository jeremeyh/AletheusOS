"""
Agent Society Models

Genesis 13.51
"""

from dataclasses import dataclass


@dataclass
class Agent:
    agent_id: str

    name: str

    specialty: str

    reputation: int = 0


@dataclass
class AgentMessage:
    sender: str

    receiver: str

    message: dict
