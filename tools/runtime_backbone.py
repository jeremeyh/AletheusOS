from aletheus.runtime.boot_pipeline import RuntimeBootPipelineReporter
from aletheus.runtime.catalyst import CatalystReporter
from aletheus.runtime.circuits import RuntimeCircuitReporter
from aletheus.runtime.composition import RuntimeCompositionRoot, RuntimeCompositionReporter
from aletheus.runtime.executive import ExecutiveKernelReporter
from aletheus.runtime.relay import RelayNetworkReporter
from aletheus.runtime.service_mesh import RuntimeServiceMeshReporter


def configure_boot_pipeline(pipeline):
    stages = [
        ("foundation", 0, [], ["runtime_foundation"]),
        ("executive_kernel", 1, ["foundation"], ["coordination"]),
        ("registries", 2, ["executive_kernel"], ["runtime_registry"]),
        ("runtime_anchor_circuits", 3, ["registries"], ["attachment_layer"]),
        ("service_mesh", 4, ["runtime_anchor_circuits"], ["runtime_topology"]),
        ("relay_network", 5, ["service_mesh"], ["packet_delivery"]),
        ("catalyst", 6, ["service_mesh"], ["runtime_optimization"]),
        ("platform_services", 7, ["relay_network", "catalyst"], ["platform_services"]),
        ("applications", 8, ["platform_services"], ["application_runtime"]),
    ]

    def handler(stage):
        return {
            "stage": stage.name,
            "provided": stage.provides,
            "status": "ok",
        }

    for name, order, dependencies, provides in stages:
        pipeline.register_stage(
            name=name,
            order=order,
            handler=handler,
            dependencies=dependencies,
            provides=provides,
        )

    return pipeline


def configure_executive_kernel(kernel):
    kernel.activate_service("Runtime Boot Pipeline")
    kernel.activate_service("Runtime Lifecycle Manager")
    kernel.activate_service("Runtime Registration Manager")
    kernel.activate_service("Runtime Command Registry")
    kernel.activate_service("Runtime Anchor Circuits")
    kernel.activate_service("Runtime Service Mesh")
    kernel.activate_service("Runtime Relay Network")
    kernel.activate_service("Catalyst")

    kernel.register_mission("Reduce runtime core responsibility")

    return kernel


def configure_circuits(manager):
    circuits = [
        ("runtime_registry", "Runtime Registry", []),
        ("boot_pipeline", "Runtime Boot Pipeline", ["runtime_registry"]),
        ("lifecycle", "Runtime Lifecycle Manager", ["runtime_registry"]),
        ("registration", "Runtime Registration Manager", ["runtime_registry"]),
        ("command_registry", "Runtime Command Registry", ["registration"]),
        ("service_mesh", "Runtime Service Mesh", ["runtime_registry"]),
        ("relay_network", "Runtime Relay Network", ["service_mesh"]),
        ("catalyst", "Catalyst Optimization Layer", ["service_mesh"]),
        ("executive_kernel", "Executive Kernel", ["runtime_registry"]),
    ]

    for name, capability, dependencies in circuits:
        manager.register_circuit(
            name=name,
            capability=capability,
            dependencies=dependencies,
        )

    for name, _, _ in circuits:
        manager.activate(name)

    return manager


def configure_mesh(mesh):
    mesh.register_node("boot_pipeline", node_type="startup")
    mesh.register_node("executive_kernel", node_type="coordinator")
    mesh.register_node("lifecycle", node_type="state_manager")
    mesh.register_node("registration", node_type="registry")
    mesh.register_node("command_registry", node_type="registry")
    mesh.register_node("runtime_registry", node_type="registry")
    mesh.register_node("runtime_anchor_circuits", node_type="attachment")
    mesh.register_node("relay_network", node_type="transport")
    mesh.register_node("catalyst", node_type="optimizer")

    return mesh


def configure_relay(relay):
    relay.register(
        "runtime_registry",
        lambda payload: {
            "service": "Runtime Registry",
            "received": True,
            "payload": payload,
        },
    )

    relay.register(
        "catalyst",
        lambda payload: {
            "service": "Catalyst",
            "optimized": True,
            "payload": payload,
        },
    )

    relay.send(
        source="executive_kernel",
        target="runtime_registry",
        payload={"action": "health"},
    )

    relay.send(
        source="executive_kernel",
        target="catalyst",
        payload={"action": "warm_routes"},
    )

    return relay


def configure_registration(manager):
    manager.register("service", "Runtime Boot Pipeline")
    manager.register("service", "Executive Kernel")
    manager.register("service", "Runtime Lifecycle Manager")
    manager.register("service", "Runtime Command Registry")
    manager.register("service", "Runtime Anchor Circuits")
    manager.register("service", "Runtime Service Mesh")
    manager.register("service", "Runtime Relay Network")
    manager.register("service", "Catalyst")
    return manager


def configure_commands(registry):
    registry.register(
        name="runtime.health",
        category="runtime",
        description="Return runtime health.",
        handler=lambda payload: {
            "runtime": "healthy",
            "payload": payload,
        },
    )

    registry.register(
        name="runtime.boot",
        category="lifecycle",
        description="Execute runtime boot pipeline.",
        handler=lambda payload: {
            "boot": "accepted",
            "payload": payload,
        },
    )

    return registry


def main():
    composition = RuntimeCompositionRoot().build()

    boot_pipeline = configure_boot_pipeline(composition.services["boot_pipeline"])
    kernel = configure_executive_kernel(composition.services["executive_kernel"])
    circuits = configure_circuits(composition.services["circuits"])
    mesh = configure_mesh(composition.services["service_mesh"])
    relay = configure_relay(composition.services["relay_network"])
    registration = configure_registration(composition.services["registration"])
    commands = configure_commands(composition.services["command_registry"])
    catalyst = composition.services["catalyst"]

    boot_report = boot_pipeline.execute()
    catalyst_report = catalyst.analyze_mesh(mesh)

    sections = [
        RuntimeCompositionReporter().render(composition),
        RuntimeBootPipelineReporter().render(boot_report),
        ExecutiveKernelReporter().render(kernel),
        RuntimeCircuitReporter().render(circuits),
        RuntimeServiceMeshReporter().render(mesh),
        RelayNetworkReporter().render(relay),
        CatalystReporter().render(catalyst_report),
    ]

    print("\n\n".join(sections))


if __name__ == "__main__":
    main()
