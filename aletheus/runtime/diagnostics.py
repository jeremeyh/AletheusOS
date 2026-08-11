from __future__ import annotations

from typing import Any


class RuntimeDiagnostics:
    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime

    def report(self) -> dict[str, Any]:
        services = list(self.runtime.services.list())

        runtime_services = [
            ("memory_mesh", "Aletheus Universal Memory Mesh"),
            ("knowledge_graph", "Aletheus Knowledge Graph Engine"),
            ("reasoning", "Aletheus Cognitive Reasoning Engine"),
            ("decision", "Aletheus Autonomous Decision Engine"),
            ("agents_v2", "Aletheus Autonomous Agent Runtime"),
            ("workflow_v3", "Aletheus Workflow Intelligence Engine"),
            ("planning_v2", "Aletheus Autonomous Planning Engine"),
            ("distributed_v3", "Aletheus Distributed Runtime Fabric"),
            ("plugins_v3", "Aletheus Plugin Manager"),
            ("persistence_v3", "Aletheus Persistence Engine"),
            ("event_bus_v3", "Aletheus Event Bus"),
            ("federation_v3", "Aletheus Federated Knowledge Fabric"),
            ("telemetry_v3", "Aletheus Observability Platform"),
            ("high_availability_v3", "Aletheus High Availability Platform"),
            ("security_v3", "Aletheus Security & Policy Engine"),
            ("tenancy_v3", "Aletheus Multi-Tenant Runtime"),
            ("distributed", "Aletheus Distributed Intelligence Fabric"),
            ("enterprise", "Aletheus Enterprise Intelligence Platform"),
            ("workflow_v2", "Aletheus v2 Autonomous Workflow Fabric"),
            ("mission_v2", "Aletheus v2 Autonomous Mission Engine"),
            ("kernel_v2", "Aletheus v2 Autonomous Kernel"),
            ("prediction", "Aletheus Predictive Intelligence Layer"),
            ("learning", "Aletheus Adaptive Learning Engine"),
            ("semantic", "Aletheus Semantic Intelligence Layer"),
            ("executive", "Aletheus Executive Intelligence Layer"),
            ("copilot", "Aletheus Founder Copilot"),
            ("planning", "Aletheus Autonomous Planning Engine"),
            ("agents", "Aletheus Multi-Agent Orchestration Layer"),
        ]

        for attr, service_name in runtime_services:
            if hasattr(self.runtime, attr) and service_name not in services:
                services.append(service_name)

        services = sorted(set(services))

        return {
            "status": "healthy",
            "version": self.runtime.version,
            "engines": self.runtime.engines.list(),
            "services": services,
            "commands": self.runtime.commands.list(),
            "pipelines": self.runtime.pipelines.list(),
            "workflows": self.runtime.workflows.list(),
            "events_count": self.runtime.events.count(),
            "metrics_count": self.runtime.metrics.count(),
            "jobs": self.runtime.scheduler.list(),
            "queue": self.runtime.queue.list(),
            "plugins": self.runtime.plugins.list(),
        }
