from aletheus.runtime.circuits import RuntimeCircuitManager, RuntimeCircuitReporter


def main():
    manager = RuntimeCircuitManager()

    manager.register_circuit(
        name="runtime_registry",
        capability="Runtime Registry",
    )

    manager.register_circuit(
        name="service_mesh",
        capability="Runtime Service Mesh",
        dependencies=["runtime_registry"],
    )

    manager.register_circuit(
        name="relay_network",
        capability="Runtime Relay Network",
        dependencies=["service_mesh"],
    )

    manager.register_circuit(
        name="catalyst",
        capability="Catalyst Optimization Layer",
        dependencies=["service_mesh"],
    )

    manager.register_circuit(
        name="governance",
        capability="Governance",
        dependencies=["runtime_registry"],
    )

    manager.register_circuit(
        name="memory",
        capability="Memory",
        dependencies=["runtime_registry"],
    )

    for circuit in [
        "runtime_registry",
        "service_mesh",
        "relay_network",
        "catalyst",
        "governance",
        "memory",
    ]:
        manager.activate(circuit)

    print(RuntimeCircuitReporter().render(manager))


if __name__ == "__main__":
    main()
