from __future__ import annotations

from aletheus.time_utils import utc_now, utc_now_iso

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any
import uuid


def utc_now() -> str:
    return utc_now_iso()


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    message: str
    created_at: str = field(default_factory=utc_now)


@dataclass
class Agent:
    name: str
    role: str

    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "idle"
    mission: str = ""
    priority: int = 0
    state: str = "ready"

    created_at: str = field(default_factory=utc_now)
    last_active: str = field(default_factory=utc_now)

    heartbeat_count: int = 0
    tasks_completed: int = 0

    inbox: List[AgentMessage] = field(default_factory=list)

    def heartbeat(self):
        self.heartbeat_count += 1
        self.last_active = utc_now()

    def assign(self, mission: str):
        self.mission = mission
        self.status = "working"
        self.last_active = utc_now()

    def pause(self):
        self.status = "paused"

    def resume(self):
        self.status = "working"

    def stop(self):
        self.status = "stopped"

    def complete(self):
        self.tasks_completed += 1
        self.status = "idle"
        self.mission = ""

    def receive(self, sender: str, message: str):
        self.inbox.append(
            AgentMessage(
                sender=sender,
                recipient=self.name,
                message=message,
            )
        )

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "status": self.status,
            "mission": self.mission,
            "priority": self.priority,
            "state": self.state,
            "heartbeat": self.heartbeat_count,
            "tasks_completed": self.tasks_completed,
            "messages": len(self.inbox),
            "created_at": self.created_at,
            "last_active": self.last_active,
        }


class AletheusAutonomousAgentRuntime:

    VERSION = "2.7.0"

    def __init__(self):

        self.agents: Dict[str, Agent] = {}


    def register_default_agents(self):
        """
        Backwards-compatible alias expected by the runtime.
        """
        return self.bootstrap()

    def bootstrap(self):

        defaults = [
            ("Founder Agent", "Founder"),
            ("Research Agent", "Research"),
            ("Marketplace Agent", "Marketplace"),
            ("Portfolio Agent", "Portfolio"),
            ("Operations Agent", "Operations"),
        ]

        for name, role in defaults:
            self.spawn(name, role)

        return self.statistics()

    def spawn(self, name: str, role: str):

        agent = Agent(name=name, role=role)

        self.agents[agent.agent_id] = agent

        return agent.to_dict()

    def assign(self, agent_id: str, mission: str):

        agent = self.agents[agent_id]

        agent.assign(mission)

        return agent.to_dict()

    def pause(self, agent_id: str):

        self.agents[agent_id].pause()

        return self.agents[agent_id].to_dict()

    def resume(self, agent_id: str):

        self.agents[agent_id].resume()

        return self.agents[agent_id].to_dict()

    def stop(self, agent_id: str):

        self.agents[agent_id].stop()

        return self.agents[agent_id].to_dict()

    def heartbeat(self):

        for agent in self.agents.values():
            agent.heartbeat()

        return self.statistics()

    def message(self, sender: str, recipient: str, message: str):

        for agent in self.agents.values():

            if agent.name == recipient:

                agent.receive(sender, message)

                return agent.to_dict()

        return {"error": "Recipient not found"}



    def status(self):
        return {
            "agents": [a.to_dict() for a in self.agents.values()]
        }

    def list_agents(self):
        return [a.to_dict() for a in self.agents.values()]



    def stats(self):
        """
        Genesis 7.9 Contract Convergence™

        Compatibility wrapper for legacy runtime callers.
        """

        data = self.statistics()

        return {
            **data,
            "online_agents": data["running"] + data["idle"],
            "offline_agents": data["stopped"],
            "tasks": data["tasks_completed"],
        }

    def statistics(self):

        return {
            "version": self.VERSION,
            "agents": len(self.agents),
            "running": sum(a.status == "working" for a in self.agents.values()),
            "idle": sum(a.status == "idle" for a in self.agents.values()),
            "paused": sum(a.status == "paused" for a in self.agents.values()),
            "stopped": sum(a.status == "stopped" for a in self.agents.values()),
            "messages": sum(len(a.inbox) for a in self.agents.values()),
            "heartbeats": sum(a.heartbeat_count for a in self.agents.values()),
            "tasks_completed": sum(a.tasks_completed for a in self.agents.values()),
        }


agent_core = AletheusAutonomousAgentRuntime()
