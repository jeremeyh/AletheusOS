from aletheus.runtime.service_mesh import RuntimeServiceMesh, RuntimeServiceMeshReporter


def memory_handler(payload):
    return {
        "service": "Memory",
        "received": True,
        "payload": payload,
    }


def governance_handler(payload):
    return {
        "service": "Governance",
        "validated": True,
        "payload": payload,
    }


def main():
    mesh = RuntimeServiceMesh()

    mesh.register_node("memory", node_type="platform_service", handler=memory_handler)
    mesh.register_node("governance", node_type="platform_service", handler=governance_handler)
    mesh.register_node("runtime_registry", node_type="registry")
    mesh.register_node("relay_network", node_type="transport")
    mesh.register_node("catalyst", node_type="optimizer")

    mesh.route(
        source="executive_kernel",
        destination="memory",
        payload={"action": "recall", "key": "platform_state"},
    )

    mesh.route(
        source="executive_kernel",
        destination="governance",
        payload={"action": "validate", "principle": "Principle X"},
    )

    print(RuntimeServiceMeshReporter().render(mesh))


if __name__ == "__main__":
    main()
