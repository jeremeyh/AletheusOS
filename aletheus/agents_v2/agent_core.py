from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime


def utc_now() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class AgentMessage:
    sender: str
    recipient: str
    message: str
    created_at: str = field(default_factory=utc_now)


@dataclass
class CompatibilityAgentTask:
    agent_name: str
    title: str
    payload: dict = field(default_factory=dict)

    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "queued"
    created_at: str = field(default_factory=utc_now)
    completed_at: str | None = None

    def complete(self):
        self.status = "completed"
        self.completed_at = utc_now()

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "agent_name": self.agent_name,
            "title": self.title,
            "payload": self.payload,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }


@dataclass
class Agent:
    name: str
    role: str

    # Historical Agent V1 compatibility metadata.
    description: str = ""
    capabilities: list[dict[str, object]] = field(default_factory=list)

    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = "idle"
    mission: str = ""
    priority: int = 0
    state: str = "ready"

    created_at: str = field(default_factory=utc_now)
    last_active: str = field(default_factory=utc_now)

    heartbeat_count: int = 0
    tasks_completed: int = 0

    inbox: list[AgentMessage] = field(default_factory=list)

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
            "description": self.description,
            "capabilities": [dict(item) for item in self.capabilities],
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

        self.agents: dict[str, Agent] = {}
        self._compat_tasks: dict[str, list[CompatibilityAgentTask]] = {}

    def register_agent(
        self,
        name: str,
        role: str,
        description: str = "",
        capabilities: list[dict[str, object]] | None = None,
    ) -> Agent:
        """
        Historical Agent V1 compatibility adapter.

        Preserves the legacy register_agent contract while storing the
        canonical Agent V2 representation.
        """
        existing = self._get_agent_by_name(name)
        if existing:
            return existing

        normalized_capabilities = [
            {
                "name": item.get("name", "Unnamed Capability"),
                "description": item.get("description", ""),
            }
            for item in (capabilities or [])
        ]

        agent = Agent(
            name=name,
            role=role,
            description=description,
            capabilities=normalized_capabilities,
        )
        self.agents[agent.agent_id] = agent
        return agent

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

    def _get_agent_by_name(self, name: str):
        for agent in self.agents.values():
            if agent.name == name:
                return agent
        return None

    def assign_task(
        self,
        agent_name: str,
        title: str,
        payload: dict | None = None,
    ):
        agent = self._get_agent_by_name(agent_name)
        if agent is None:
            return None

        task = CompatibilityAgentTask(
            agent_name=agent_name,
            title=title,
            payload=payload or {},
        )

        self._compat_tasks.setdefault(agent.agent_id, []).append(task)

        # Preserve the native v2 mission/state model.
        agent.assign(title)

        return task

    def run_agent(self, agent_name: str):
        agent = self._get_agent_by_name(agent_name)

        if agent is None:
            return {"error": f"Agent not found: {agent_name}"}

        queue = self._compat_tasks.setdefault(agent.agent_id, [])

        task = next(
            (candidate for candidate in queue if candidate.status == "queued"),
            None,
        )

        if task is None:
            return {
                "message": "No queued tasks.",
                "agent": agent.name,
            }

        task.complete()
        agent.complete()

        return task.to_dict()

    def orchestrate(
        self,
        objective: str,
        participating_agents: list[str] | None = None,
    ):
        agents = participating_agents or [
            agent.name for agent in self.agents.values()
        ]

        assignments = []

        for agent_name in agents:
            task = self.assign_task(
                agent_name=agent_name,
                title=f"Contribute to objective: {objective}",
                payload={"objective": objective},
            )

            if task is not None:
                assignments.append(
                    {
                        "agent": agent_name,
                        "task": task.to_dict(),
                    }
                )

        results = []

        for agent_name in agents:
            results.append(
                {
                    "agent": agent_name,
                    "result": self.run_agent(agent_name),
                }
            )

        return {
            "objective": objective,
            "assignments": assignments,
            "results": results,
        }

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
        return {"agents": [a.to_dict() for a in self.agents.values()]}

    def list_agents(self):
        return [a.to_dict() for a in self.agents.values()]

    def stats(self):
        return self.statistics()

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
