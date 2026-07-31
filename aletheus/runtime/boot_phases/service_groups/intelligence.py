class IntelligenceServiceRegistrar:
    def register(self, runtime):
        runtime.services.register(
            "Aletheus Semantic Intelligence Layer",
            {"status": "online", "version": runtime.semantic.version},
        )

        runtime.services.register(
            "Aletheus Executive Intelligence Layer",
            {"status": "online", "version": runtime.executive.version},
        )

        runtime.services.register(
            "Aletheus Multi-Agent Orchestration Layer",
            {"status": "online", "version": runtime.agents_v2.VERSION},
        )

        runtime.services.register(
            "Aletheus Autonomous Planning Engine",
            {"status": "online", "version": runtime.planning_v2.VERSION},
        )

        return 4
