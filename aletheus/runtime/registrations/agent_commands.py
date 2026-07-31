"""
Agent Command Registration.

Exposes the canonical autonomous-agent lifecycle and preserves the
historical v1.3 task/orchestration command surface.
"""

from __future__ import annotations

from typing import Any

from aletheus.runtime.domains import AgentDomain


def _serialize(value: Any) -> Any:
    if value is None:
        return None

    if hasattr(value, "to_dict"):
        return value.to_dict()

    if hasattr(value, "__dict__"):
        return dict(value.__dict__)

    return value


def register_agent_commands(runtime):
    commands = runtime.commands
    domain = AgentDomain(runtime)
    agents = runtime.agents_v2

    def find_agent_by_name(name: str):
        for agent in agents.agents.values():
            if agent.name == name:
                return agent

        return None

    def ensure_default_agents() -> None:
        if not agents.agents:
            agents.bootstrap()

        required = {
            "Executive Agent": "Executive",
            "Knowledge Agent": "Knowledge",
            "Memory Agent": "Memory",
            "Market Agent": "Marketplace",
            "Operations Agent": "Operations",
            "Research Agent": "Research",
        }

        existing = {agent.name for agent in agents.agents.values()}

        for name, role in required.items():
            if name not in existing:
                agents.spawn(
                    name=name,
                    role=role,
                )

    def assign_task(payload=None):
        payload = payload or {}

        ensure_default_agents()

        agent_name = payload.get(
            "agent_name",
            "Executive Agent",
        )

        agent = find_agent_by_name(agent_name)

        if agent is None:
            raise KeyError(f"Agent not found: {agent_name}")

        title = payload.get(
            "title",
            "Untitled Agent Task",
        )

        task_payload = payload.get(
            "payload",
            {},
        )

        agent.assign(title)

        task = {
            "task_id": (f"{agent.agent_id}:{agent.tasks_completed + 1}"),
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "title": title,
            "payload": task_payload,
            "status": "assigned",
        }

        return task

    def run_agent(payload=None):
        payload = payload or {}

        ensure_default_agents()

        agent_name = payload.get(
            "agent_name",
            "Executive Agent",
        )

        agent = find_agent_by_name(agent_name)

        if agent is None:
            raise KeyError(f"Agent not found: {agent_name}")

        mission = agent.mission

        if not mission:
            mission = "No pending mission"

        result = {
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "role": agent.role,
            "mission": mission,
            "status": "completed",
            "result": {
                "summary": (f"{agent.name} completed: {mission}"),
                "confidence": 0.85,
            },
        }

        agent.complete()

        return result

    def orchestrate(payload=None):
        payload = payload or {}

        ensure_default_agents()

        objective = payload.get(
            "objective",
            "",
        )

        requested = payload.get("participating_agents")

        if requested:
            selected = [
                agent for agent in agents.agents.values() if agent.name in requested
            ]
        else:
            selected = list(agents.agents.values())

        results = []

        for agent in selected:
            agent.assign(objective)

            results.append(
                {
                    "agent_id": agent.agent_id,
                    "agent_name": agent.name,
                    "role": agent.role,
                    "objective": objective,
                    "status": "completed",
                    "contribution": (
                        f"{agent.name} evaluated "
                        f"the objective from the "
                        f"{agent.role} perspective."
                    ),
                    "confidence": 0.82,
                }
            )

            agent.complete()

        return {
            "objective": objective,
            "status": "completed",
            "participants": len(results),
            "results": results,
        }

    # Canonical v2.7 agent lifecycle
    commands.register(
        "agent.bootstrap",
        domain.bootstrap,
        replace=True,
    )
    commands.register(
        "agent.spawn",
        domain.spawn,
        replace=True,
    )
    commands.register(
        "agent.assign",
        domain.assign,
        replace=True,
    )
    commands.register(
        "agent.message",
        domain.message,
        replace=True,
    )
    commands.register(
        "agent.pause",
        domain.pause,
        replace=True,
    )
    commands.register(
        "agent.resume",
        domain.resume,
        replace=True,
    )
    commands.register(
        "agent.stop",
        domain.stop,
        replace=True,
    )
    commands.register(
        "agent.heartbeat",
        domain.heartbeat,
        replace=True,
    )
    commands.register(
        "agent.statistics",
        domain.statistics,
        replace=True,
    )

    # Historical v1.3 compatibility surface
    commands.register(
        "agent.task.assign",
        assign_task,
        replace=True,
    )
    commands.register(
        "agent.run",
        run_agent,
        replace=True,
    )
    commands.register(
        "agent.orchestrate",
        orchestrate,
        replace=True,
    )
