class FoundationServiceRegistrar:

    def register(self, runtime):
        runtime.services.register(
            "Aletheus Autonomous Mission Engine",
            {"status": "online", "version": runtime.mission.version},
        )

        runtime.services.register(
            "Aletheus Founder Workspace",
            {"status": "online", "version": runtime.workspace.version},
        )

        runtime.services.register(
            "Aletheus Native Application Manager",
            {"status": "online", "version": runtime.applications.version},
        )

        runtime.services.register(
            "Aletheus Genesis Release Core",
            {"status": "online", "version": runtime.release.manifest.version},
        )

        return 4
