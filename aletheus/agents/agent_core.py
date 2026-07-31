from __future__ import annotations

from typing import Any

from aletheus.agents.models import AgentCapability, AgentTask, AletheusAgent


class AletheusAgentCore:
    def __init__(self) -> None:
        self.version = "1.3.0"
        self.agents: list[AletheusAgent] = []

    def register_agent(
        self,
        name: str,
        role: str,
        description: str = "",
        capabilities: list[dict[str, Any]] | None = None,
    ) -> AletheusAgent:
        existing = self.get_agent(name=name)
        if existing:
            return existing

        agent = AletheusAgent(
            name=name,
            role=role,
            description=description,
            capabilities=[
                AgentCapability(
                    name=item.get("name", "Unnamed Capability"),
                    description=item.get("description", ""),
                )
                for item in (capabilities or [])
            ],
        )
        self.agents.append(agent)
        return agent

    def register_default_agents(self) -> list[dict[str, Any]]:
        defaults = [
            {
                "name": "Executive Agent",
                "role": "executive",
                "description": "Synthesizes system state, priorities, recommendations, and risks.",
                "capabilities": [
                    {
                        "name": "executive_summary",
                        "description": "Create executive summaries.",
                    },
                    {"name": "risk_review", "description": "Analyze system risks."},
                ],
            },
            {
                "name": "Memory Agent",
                "role": "memory",
                "description": "Manages memory recall, consolidation, and memory hygiene.",
                "capabilities": [
                    {"name": "recall", "description": "Retrieve relevant memories."},
                    {
                        "name": "consolidate",
                        "description": "Prepare records for long-term memory.",
                    },
                ],
            },
            {
                "name": "Knowledge Agent",
                "role": "knowledge",
                "description": "Expands graph entities, relationships, and semantic assertions.",
                "capabilities": [
                    {"name": "graph_expand", "description": "Expand knowledge graph."},
                    {
                        "name": "semantic_linking",
                        "description": "Link semantic assertions.",
                    },
                ],
            },
            {
                "name": "Scout Agent",
                "role": "scout",
                "description": "Finds opportunities, targets, listings, and market signals.",
                "capabilities": [
                    {
                        "name": "opportunity_search",
                        "description": "Search for acquisition opportunities.",
                    },
                    {
                        "name": "watchlist_scan",
                        "description": "Scan watchlists and candidate pools.",
                    },
                ],
            },
            {
                "name": "Market Agent",
                "role": "market",
                "description": "Analyzes pricing, valuation, volatility, and comps.",
                "capabilities": [
                    {"name": "pricing", "description": "Analyze price signal."},
                    {"name": "valuation", "description": "Estimate value and risk."},
                ],
            },
            {
                "name": "Founder Agent",
                "role": "founder",
                "description": "Coordinates founder workflow, priorities, notes, and decisions.",
                "capabilities": [
                    {
                        "name": "daily_workflow",
                        "description": "Organize founder priorities.",
                    },
                    {
                        "name": "decision_capture",
                        "description": "Capture decisions and rationale.",
                    },
                ],
            },
        ]

        return [
            self.register_agent(
                name=item["name"],
                role=item["role"],
                description=item["description"],
                capabilities=item["capabilities"],
            ).to_dict()
            for item in defaults
        ]

    def get_agent(self, agent_id: str = "", name: str = "") -> AletheusAgent | None:
        for agent in self.agents:
            if agent_id and agent.agent_id == agent_id:
                return agent
            if name and agent.name == name:
                return agent
        return None

    def list_agents(self) -> list[dict[str, Any]]:
        return [agent.to_dict() for agent in self.agents]

    def assign_task(
        self,
        agent_name: str,
        title: str,
        payload: dict[str, Any] | None = None,
    ) -> AgentTask | None:
        agent = self.get_agent(name=agent_name)
        if agent is None:
            return None
        return agent.assign_task(title=title, payload=payload or {})

    def run_agent(self, agent_name: str) -> dict[str, Any]:
        agent = self.get_agent(name=agent_name)
        if agent is None:
            return {"error": f"Agent not found: {agent_name}"}

        task = agent.complete_next_task()
        if task is None:
            return {"message": "No queued tasks.", "agent": agent.name}

        return task.to_dict()

    def orchestrate(
        self,
        objective: str,
        participating_agents: list[str] | None = None,
    ) -> dict[str, Any]:
        agents = participating_agents or [
            "Executive Agent",
            "Memory Agent",
            "Knowledge Agent",
            "Scout Agent",
            "Market Agent",
            "Founder Agent",
        ]

        assignments = []
        for agent_name in agents:
            task = self.assign_task(
                agent_name=agent_name,
                title=f"Contribute to objective: {objective}",
                payload={"objective": objective},
            )
            if task:
                assignments.append({"agent": agent_name, "task": task.to_dict()})

        results = []
        for agent_name in agents:
            results.append({"agent": agent_name, "result": self.run_agent(agent_name)})

        return {
            "objective": objective,
            "assignments": assignments,
            "results": results,
        }

    def stats(self) -> dict[str, Any]:
        tasks = [task for agent in self.agents for task in agent.tasks]
        return {
            "version": self.version,
            "agents": len(self.agents),
            "online_agents": len(
                [agent for agent in self.agents if agent.status == "online"]
            ),
            "tasks": len(tasks),
            "queued_tasks": len([task for task in tasks if task.status == "queued"]),
            "completed_tasks": len(
                [task for task in tasks if task.status == "completed"]
            ),
        }


agent_core = AletheusAgentCore()
