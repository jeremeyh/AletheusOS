from aletheus.runtime.relay import RelayNetwork, RelayNetworkReporter


def runtime_registry_handler(payload):
    return {
        "received": True,
        "service": "Runtime Registry",
        "payload": payload,
    }


def catalyst_handler(payload):
    return {
        "received": True,
        "service": "Catalyst",
        "optimized": True,
        "payload": payload,
    }


def main():
    network = RelayNetwork()

    network.register("runtime_registry", runtime_registry_handler)
    network.register("catalyst", catalyst_handler)

    network.send(
        source="executive_kernel",
        target="runtime_registry",
        payload={"action": "health"},
    )

    network.send(
        source="executive_kernel",
        target="catalyst",
        payload={"action": "optimize_route", "route": "default"},
    )

    print(RelayNetworkReporter().render(network))


if __name__ == "__main__":
    main()
