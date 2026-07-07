from aletheus.capability_graph import (
    bootstrap_graph,
    CapabilityGraphReporter,
)


def main():
    graph = bootstrap_graph()
    print(CapabilityGraphReporter().render(graph))


if __name__ == "__main__":
    main()
