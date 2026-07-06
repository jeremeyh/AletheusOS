from __future__ import annotations

from typing import List

from .registry import uci
from .models import UCINode, UCIRelationship


def find_nodes_by_tag(tag: str) -> List[UCINode]:
    tag = tag.lower()

    return [
        node
        for node in uci.all_nodes()
        if tag in [t.lower() for t in node.tags]
    ]


def find_nodes_by_type(node_type: str) -> List[UCINode]:
    return [
        node
        for node in uci.all_nodes()
        if node.node_type.value == node_type
    ]


def relationships_for_node(node_id: str) -> List[UCIRelationship]:
    return (
        uci.incoming_relationships(node_id)
        + uci.outgoing_relationships(node_id)
    )


def explain_node(node_id: str) -> dict:
    node = uci.get_node(node_id)

    if not node:
        return {
            "found": False,
            "node_id": node_id,
            "message": "Node not found in Unified Cognitive Index.",
        }

    incoming = uci.incoming_relationships(node_id)
    outgoing = uci.outgoing_relationships(node_id)

    return {
        "found": True,
        "node": node,
        "incoming_relationships": incoming,
        "outgoing_relationships": outgoing,
        "relationship_count": len(incoming) + len(outgoing),
    }
