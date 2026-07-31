class CoreServiceRegistrar:
    def register(self, runtime):
        runtime.services.register(
            "Aletheus Runtime Core",
            {"status": "online", "version": runtime.version},
        )

        runtime.services.register(
            "Aletheus Memory Core",
            {"status": "online", "version": runtime.memory.version},
        )

        runtime.services.register(
            "Aletheus Cognition Core",
            {"status": "online", "version": runtime.cognition.version},
        )

        runtime.services.register(
            "Aletheus Knowledge Graph Engine",
            {"status": "online", "version": runtime.knowledge.version},
        )

        return 4
