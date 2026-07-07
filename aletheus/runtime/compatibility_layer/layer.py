class CompatibilityLayer:
    """
    Compatibility Layer™

    Owns runtime compatibility bootstrap, service alias registration,
    and safe compatibility alias application.

    The runtime should ask this layer to bootstrap compatibility instead
    of owning compatibility wiring directly.
    """

    SERVICE_REGISTRY = [
        ("memory", ["memory"]),
        ("knowledge", ["knowledge"]),
        ("reasoning", ["reasoning"]),
        ("decision", ["decision"]),
        ("planning", ["planning_v2", "planning"]),
        ("workflow", ["workflow_v3", "workflow_v2", "workflow"]),
        ("agents", ["agents_v2", "agents"]),
        ("plugins", ["plugins_v3"]),
        ("persistence", ["persistence_v3"]),
        ("events", ["event_bus_v3"]),
        ("federation", ["federation_v3"]),
        ("telemetry", ["telemetry_v3"]),
        ("ha", ["high_availability_v3"]),
        ("security", ["security_v3"]),
        ("tenancy", ["tenancy_v3"]),
    ]

    SAFE_ALIASES = [
        "memory",
        "knowledge",
        "reasoning",
        "decision",
        "planning",
        "workflow",
        "agents",
        "security",
        "tenancy",
    ]

    def __init__(self, registry):
        self.registry = registry

    def bootstrap(self, runtime):
        self.registry.services.clear()
        self.register_services(runtime)
        self.apply_aliases(runtime)

        return {
            "status": "bootstrapped",
            "services": self.registry.list(),
        }

    def register_services(self, runtime):
        for alias, attrs in self.SERVICE_REGISTRY:
            service = None

            for attr in attrs:
                candidate = getattr(runtime, attr, None)

                if candidate is not None:
                    service = candidate
                    break

            if service is not None:
                self.registry.register(
                    alias=alias,
                    implementation=service,
                )

    def apply_aliases(self, runtime):
        for alias in self.SAFE_ALIASES:
            try:
                setattr(runtime, alias, self.registry.resolve(alias))
            except KeyError:
                pass

        try:
            runtime.high_availability = self.registry.resolve("ha")
        except KeyError:
            pass

        try:
            runtime.event_bus = self.registry.resolve("events")
        except KeyError:
            pass

    def list(self):
        return self.registry.list()

    def statistics(self):
        return self.registry.statistics()

    def resolve(self, alias):
        return self.registry.resolve(alias)

    def contract(self, alias):
        service = self.registry.resolve(alias)

        return {
            "name": alias,
            "version": getattr(
                service,
                "VERSION",
                getattr(service, "version", "unknown"),
            ),
            "implementation": type(service).__name__,
        }
