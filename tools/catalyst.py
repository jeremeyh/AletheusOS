from aletheus.runtime.catalyst import CatalystOptimizer, CatalystReporter
from aletheus.runtime.service_mesh import RuntimeServiceMesh


def main():
    mesh = RuntimeServiceMesh()

    mesh.register_node(
        "memory", node_type="platform_service", handler=lambda payload: {"ok": True}
    )
    mesh.register_node(
        "governance", node_type="platform_service", handler=lambda payload: {"ok": True}
    )
    mesh.register_node("runtime_registry", node_type="registry")
    mesh.register_node("relay_network", node_type="transport")
    mesh.register_node("executive_kernel", node_type="coordinator")

    optimizer = CatalystOptimizer()
    report = optimizer.analyze_mesh(mesh)

    print(CatalystReporter().render(report))


if __name__ == "__main__":
    main()
