class RuntimeAgentBootPhase:
    """
    Runtime Agent Boot Phase™

    Boots built-in autonomous agents.
    """

    def run(self, runtime):

        runtime.agents.register_default_agents()

        return {
            "agents": [
                "Default Agents",
            ],
        }
