from aletheus.capability_graph import (
    CapabilityGraphReporter,
    bootstrap_graph,
)


def main():
    graph = bootstrap_graph()
    print(CapabilityGraphReporter().render(graph))


if __name__ == "__main__":
    main()
