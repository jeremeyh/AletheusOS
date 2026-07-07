from aletheus.runtime.boot_phases.service_groups import (
    CoreServiceRegistrar,
    FoundationServiceRegistrar,
    IntelligenceServiceRegistrar,
)


class RuntimeServiceRegistrationPhase:
    """
    Runtime Service Registration Phase™

    Coordinates runtime service registration.

    Individual registrations are delegated to bounded registrars.
    """

    def __init__(self):
        self._registrars = [
            ("core", CoreServiceRegistrar()),
            ("foundation", FoundationServiceRegistrar()),
            ("intelligence", IntelligenceServiceRegistrar()),
        ]

    def run(self, runtime):
        total = 0
        completed = []

        for name, registrar in self._registrars:
            count = registrar.register(runtime)
            total += count
            completed.append(name)

        return {
            "registered": total,
            "groups": completed,
        }
