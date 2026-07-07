from aletheus.runtime.compat import compatibility_registry
from aletheus.runtime.compatibility_layer import CompatibilityLayer


class DemoService:
    VERSION = "1.0"


class DemoRuntime:
    memory = DemoService()
    knowledge = DemoService()
    reasoning = DemoService()
    planning_v2 = DemoService()
    workflow_v3 = DemoService()
    agents_v2 = DemoService()
    security_v3 = DemoService()
    tenancy_v3 = DemoService()
    event_bus_v3 = DemoService()
    high_availability_v3 = DemoService()


def main():
    runtime = DemoRuntime()

    layer = CompatibilityLayer(compatibility_registry)

    result = layer.bootstrap(runtime)

    print("========================================================")
    print("ALETHEUSOS COMPATIBILITY LAYER")
    print("========================================================")
    print()
    print(f"Status.........................{result['status']}")
    print(f"Services.......................{len(result['services'])}")
    print()
    print("========================================================")


if __name__ == "__main__":
    main()
