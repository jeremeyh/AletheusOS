class RuntimeHealthService:
    """
    Runtime Health Service™

    Extracts runtime health reporting out of runtime/core.py.

    This service reads runtime state and subsystem statistics, but does not
    mutate runtime behavior.
    """

    STAT_FIELDS = [
        ("memory", "memory_records", "total_records"),
        ("cognition", "goals", "goals"),
        ("cognition", "decisions", "decisions"),
        ("knowledge", "knowledge_entities", "entities"),
        ("knowledge", "knowledge_relationships", "relationships"),
        ("mission", "missions", "missions"),
        ("mission", "active_missions", "active_missions"),
        ("workspace", "active_objectives", "active_objectives"),
        ("workspace", "notifications", "notifications"),
        ("applications", "applications", "applications"),
        ("applications", "running_applications", "running"),
        ("semantic", "semantic_concepts", "concepts"),
        ("semantic", "semantic_assertions", "assertions"),
        ("executive", "executive_recommendations", "recommendations"),
        ("executive", "executive_risks", "risks"),
        ("agents", "agents", "agents"),
        ("agents", "online_agents", "online_agents"),
        ("agents", "agent_tasks", "tasks"),
        ("planning", "plans", "plans"),
        ("planning", "active_plans", "active_plans"),
        ("copilot", "copilot_exchanges", "exchanges"),
        ("copilot", "copilot_recommendations", "recommendations"),
        ("intelligence", "uil_contexts", "contexts"),
        ("intelligence", "uil_decisions", "decisions"),
        ("prediction", "forecasts", "forecasts"),
        ("prediction", "predictive_risks", "risks"),
        ("prediction", "predictive_opportunities", "opportunities"),
        ("learning", "learning_experiences", "experiences"),
        ("learning", "learning_score", "learning_score"),
        ("kernel_v2", "kernel_events", "events"),
        ("kernel_v2", "kernel_registry_items", "registry_items"),
        ("mission_v2", "v2_missions", "missions"),
        ("mission_v2", "v2_mission_events", "telemetry_events"),
        ("workflow_v2", "v2_workflows", "workflows"),
        ("workflow_v2", "v2_workflow_events", "events"),
        ("enterprise", "enterprises", "organizations"),
        ("enterprise", "enterprise_audit_events", "audit_events"),
        ("enterprise", "compliance_score", "compliance_score"),
        ("distributed", "distributed_clusters", "clusters"),
        ("distributed", "distributed_nodes", "nodes"),
        ("distributed", "distributed_tasks", "tasks"),
        ("memory_mesh", "memory_mesh_objects", "memory_objects"),
        ("memory_mesh", "memory_mesh_snapshots", "snapshots"),
        ("memory_mesh", "memory_mesh_versions", "memory_versions"),
        ("knowledge_graph", "graph_nodes", "nodes"),
        ("knowledge_graph", "graph_relationships", "relationships"),
        ("knowledge_graph", "inference_rules", "inference_rules"),
        ("reasoning", "reasoning_traces", "traces"),
        ("reasoning", "reasoning_rules", "rules"),
        ("reasoning", "reasoning_confidence", "confidence"),
    ]

    @staticmethod
    def _count(value):
        if hasattr(value, "count"):
            return value.count()
        return 0

    @staticmethod
    def _stats(component):
        if component is None:
            return {}

        if hasattr(component, "stats"):
            return component.stats()

        if hasattr(component, "statistics"):
            return component.statistics()

        return {
            "status": getattr(component, "status", "unknown"),
        }

    def collect(self, runtime):
        health = {
            "organization": runtime.organization,
            "product": runtime.product,
            "product_type": runtime.product_type,
            "status": runtime.status,
            "version": runtime.version,
            "engines": self._count(runtime.engines),
            "services": self._count(runtime.services),
            "commands": self._count(runtime.commands),
            "events": self._count(runtime.events),
            "metrics": self._count(runtime.metrics),
        }

        stats_cache = {}

        for attr, output_key, stat_key in self.STAT_FIELDS:
            if attr not in stats_cache:
                stats_cache[attr] = self._stats(
                    getattr(runtime, attr, None)
                )

            health[output_key] = stats_cache[attr].get(
                stat_key,
                0,
            )

        return health
