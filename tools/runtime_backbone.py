from aletheus.runtime.boot_pipeline import (
    RuntimeBootPipeline,
    RuntimeBootPipelineReporter,
)

from aletheus.runtime.catalyst import (
    CatalystOptimizer,
    CatalystReporter,
)

from aletheus.runtime.circuits import (
    RuntimeCircuitManager,
    RuntimeCircuitReporter,
)

from aletheus.runtime.executive import (
    ExecutiveKernel,
    ExecutiveKernelReporter,
)

from aletheus.runtime.relay import (
    RelayNetwork,
    RelayNetworkReporter,
)

from aletheus.runtime.service_mesh import (
    RuntimeServiceMesh,
    RuntimeServiceMeshReporter,
)


###############################################################################
# Executive Kernel
###############################################################################

def build_executive_kernel():
    kernel = ExecutiveKernel()

    kernel.activate_service("Runtime Anchor Circuits")
    kernel.activate_service("Runtime Service Mesh")
    kernel.activate_service("Runtime Relay Network")
    kernel.activate_service("Catalyst")

    kernel.register_mission(
        "Reduce runtime core responsibility"
    )

    return kernel


###############################################################################
# Runtime Circuits
###############################################################################

def build_circuits():
    manager = RuntimeCircuitManager()

    circuits = [
        ("runtime_registry", "Runtime Registry", []),
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


###############################################################################
# Runtime Service Mesh
###############################################################################

def build_mesh():
    mesh = RuntimeServiceMesh()

    mesh.register_node(
        "executive_kernel",
        node_type="coordinator",
    )

    mesh.register_node(
        "runtime_registry",
        node_type="registry",
    )

    mesh.register_node(
        "runtime_anchor_circuits",
        node_type="attachment",
    )

    mesh.register_node(
        "relay_network",
        node_type="transport",
    )

    mesh.register_node(
        "catalyst",
        node_type="optimizer",
    )

    return mesh


###############################################################################
# Relay Network
###############################################################################

def build_relay():
    relay = RelayNetwork()

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
        payload={
            "action": "health",
        },
    )

    relay.send(
        source="executive_kernel",
        target="catalyst",
        payload={
            "action": "warm_routes",
        },
    )

    return relay


###############################################################################
# Runtime Boot Pipeline
###############################################################################

def build_boot_pipeline():
    pipeline = RuntimeBootPipeline()

    stages = [
        ("foundation", 0, [], ["runtime_foundation"]),
        ("executive_kernel", 1, ["foundation"], ["coordination"]),
        ("registries", 2, ["executive_kernel"], ["runtime_registry"]),
        (
            "runtime_anchor_circuits",
            3,
            ["registries"],
            ["attachment_layer"],
        ),
        (
            "service_mesh",
            4,
            ["runtime_anchor_circuits"],
            ["runtime_topology"],
        ),
        (
            "relay_network",
            5,
            ["service_mesh"],
            ["packet_delivery"],
        ),
        (
            "catalyst",
            6,
            ["service_mesh"],
            ["runtime_optimization"],
        ),
        (
            "platform_services",
            7,
            ["relay_network", "catalyst"],
            ["platform_services"],
        ),
        (
            "applications",
            8,
            ["platform_services"],
            ["application_runtime"],
        ),
    ]

    def handler(stage):
        return {
            "stage": stage.name,
            "provided": stage.provides,
            "status": "ok",
        }

    for (
        name,
        order,
        dependencies,
        provides,
    ) in stages:
        pipeline.register_stage(
            name=name,
            order=order,
            handler=handler,
            dependencies=dependencies,
            provides=provides,
        )

    return pipeline


###############################################################################
# Main
###############################################################################

def main():
    kernel = build_executive_kernel()

    circuits = build_circuits()

    mesh = build_mesh()

    relay = build_relay()

    boot_pipeline = build_boot_pipeline()

    boot_report = boot_pipeline.execute()

    catalyst = CatalystOptimizer()

    catalyst_report = catalyst.analyze_mesh(mesh)

    sections = [
        RuntimeBootPipelineReporter().render(
            boot_report
        ),
        ExecutiveKernelReporter().render(
            kernel
        ),
        RuntimeCircuitReporter().render(
            circuits
        ),
        RuntimeServiceMeshReporter().render(
            mesh
        ),
        RelayNetworkReporter().render(
            relay
        ),
        CatalystReporter().render(
            catalyst_report
        ),
    ]

    print("\n\n".join(sections))


if __name__ == "__main__":
    main()
