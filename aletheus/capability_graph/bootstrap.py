from .graph import CapabilityGraph
from .models import CapabilityNode


def bootstrap_graph():

    graph = CapabilityGraph()

    graph.add_node(
        CapabilityNode(
            "aletheus_os",
            "AletheusOS",
            "platform",
        )
    )

    graph.add_node(
        CapabilityNode(
            "runtime",
            "Runtime",
            "platform",
        )
    )

    graph.add_node(
        CapabilityNode(
            "memory",
            "Memory",
            "platform",
        )
    )

    graph.add_node(
        CapabilityNode(
            "reasoning",
            "Reasoning",
            "platform",
        )
    )

    graph.add_node(
        CapabilityNode(
            "workflow",
            "Workflow",
            "platform",
        )
    )

    graph.add_node(
        CapabilityNode(
            "card_hawk",
            "Card Hawk",
            "application",
        )
    )

    graph.add_node(
        CapabilityNode(
            "asset_vault",
            "Asset Vault",
            "application",
        )
    )

    graph.add_node(
        CapabilityNode(
            "marketplace",
            "Marketplace Intelligence",
            "application",
        )
    )

    graph.add_node(
        CapabilityNode(
            "thorx",
            "THORᵡ",
            "application",
        )
    )

    graph.connect("aletheus_os", "runtime")
    graph.connect("aletheus_os", "memory")
    graph.connect("aletheus_os", "reasoning")
    graph.connect("aletheus_os", "workflow")
    graph.connect("aletheus_os", "card_hawk")

    graph.connect("card_hawk", "asset_vault")
    graph.connect("card_hawk", "marketplace")
    graph.connect("card_hawk", "thorx")

    return graph
