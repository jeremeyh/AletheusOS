"""
Runtime Registration Manager

Version 5.0.0
"""

from aletheus.runtime import registrations


class RegistrationManager:

    def __init__(self, runtime):
        self.runtime = runtime

    def register_all(self):

        registrations.register_runtime_commands(self.runtime)

        registrations.register_memory_commands(self.runtime)

        registrations.register_reasoning_commands(self.runtime)

        registrations.register_decision_commands(self.runtime)

        registrations.register_graph_commands(self.runtime)

        registrations.register_mission_commands(self.runtime)

        registrations.register_workspace_commands(self.runtime)

        registrations.register_application_commands(self.runtime)

        registrations.register_semantic_commands(self.runtime)

        registrations.register_executive_commands(self.runtime)

        registrations.register_agent_commands(self.runtime)

        registrations.register_planning_commands(self.runtime)

        registrations.register_copilot_commands(self.runtime)

        registrations.register_uil_commands(self.runtime)
