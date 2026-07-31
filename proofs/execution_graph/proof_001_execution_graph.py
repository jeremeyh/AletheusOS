"""
AletheusOS
Genesis 50.0

Proof 001

Foundation Execution Graph™

Constitutional Lineage Proof
"""

from __future__ import annotations

from pprint import pprint

from aletheus.execution_graph import (
    EdgeType,
    NodeType,
    foundation_execution_graph,
)


def header(title: str) -> None:

    print()
    print(title)
    print("=" * len(title))


def main() -> None:

    #
    # Build a simple constitutional execution.
    #

    intent = foundation_execution_graph.create_node(
        node_type=NodeType.INTENT,
        canonical_id="INTENT-0001",
        display_name="Card Appraisal Intent",
    )

    identity = foundation_execution_graph.create_node(
        node_type=NodeType.IDENTITY,
        canonical_id="identity.founder.master_lord_6ixth",
        display_name="Jeremey Harvey",
    )

    memory = foundation_execution_graph.create_node(
        node_type=NodeType.MEMORY,
        canonical_id="MEM-0001",
        display_name="Marketplace Observation",
    )

    reason = foundation_execution_graph.create_node(
        node_type=NodeType.REASON,
        canonical_id="REASON-0001",
        display_name="Constitutional Appraisal",
    )

    execution = foundation_execution_graph.create_node(
        node_type=NodeType.EXECUTION,
        canonical_id="EXEC-0001",
        display_name="CardHawk Execution",
    )

    #
    # Connect them.
    #

    foundation_execution_graph.connect(
        source=intent,
        target=identity,
        edge_type=EdgeType.USED,
    )

    foundation_execution_graph.connect(
        source=identity,
        target=memory,
        edge_type=EdgeType.REFERENCED,
    )

    foundation_execution_graph.connect(
        source=memory,
        target=reason,
        edge_type=EdgeType.JUSTIFIED_BY,
    )

    foundation_execution_graph.connect(
        source=reason,
        target=execution,
        edge_type=EdgeType.PRODUCED,
    )

    #
    # Output
    #

    header("GRAPH NODES")

    pprint([n.to_dict() for n in foundation_execution_graph.nodes()])

    header("GRAPH EDGES")

    pprint([e.to_dict() for e in foundation_execution_graph.edges()])

    header("LINEAGE")

    pprint(foundation_execution_graph.explain(reason.node_id))

    header("MERMAID")

    print(foundation_execution_graph.mermaid())

    header("HEALTH")

    pprint(foundation_execution_graph.health())

    header("STATISTICS")

    pprint(foundation_execution_graph.statistics())


if __name__ == "__main__":
    main()
