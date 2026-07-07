from aletheus.runtime.boot_phases.service_groups import (
    AIPlatformServiceRegistrar,
    CoreServiceRegistrar,
    FoundationServiceRegistrar,
    IntelligenceServiceRegistrar,
)


class RuntimeServiceRegistrationPhase:
    """
    Coordinates runtime service registration.
    """

    def __init__(self):
        self._registrars = [
            ("core", CoreServiceRegistrar()),
            ("foundation", FoundationServiceRegistrar()),
            ("intelligence", IntelligenceServiceRegistrar()),
            ("ai_platform", AIPlatformServiceRegistrar()),
        ]

    def run(self, runtime):
        registered = 0
        groups = []

        for name, registrar in self._registrars:
            registered += registrar.register(runtime)
            groups.append(name)

        return {
            "registered": registered,
            "groups": groups,
        }
