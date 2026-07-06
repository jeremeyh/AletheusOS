from __future__ import annotations

from collections import deque
from typing import List, Set

from .registry import uci
from .models import (
    UCITrace,
    UCIRelationship,
)


def trace_lineage(
    origin_node_id: str,
    max_depth: int = 50,
) -> UCITrace:
    """
    Walk outward through cognitive relationships and
    build a lineage trace.

    This is intentionally lightweight.

    Future versions may support weighted traversal,
    constitutional filtering,
    intent filtering,
    and confidence thresholds.
    """

    visited: Set[str] = set()

    queue = deque()

    queue.append(
        (
            origin_node_id,
            [],
            [],
        )
    )

    while queue:

        (
            current_node,
            node_path,
            relationship_path,
        ) = queue.popleft()

        if current_node in visited:
            continue

        visited.add(current_node)

        new_node_path = node_path + [current_node]

        if len(new_node_path) >= max_depth:

            return UCITrace(
                origin_node_id=origin_node_id,
                terminal_node_id=current_node,
                path=new_node_path,
                relationships=relationship_path,
            )

        outgoing: List[
            UCIRelationship
        ] = uci.outgoing_relationships(current_node)

        if not outgoing:

            return UCITrace(
                origin_node_id=origin_node_id,
                terminal_node_id=current_node,
                path=new_node_path,
                relationships=relationship_path,
            )

        for relationship in outgoing:

            queue.append(
                (
                    relationship.target_node_id,
                    new_node_path,
                    relationship_path
                    + [relationship.relationship_id],
                )
            )

    return UCITrace(
        origin_node_id=origin_node_id,
        terminal_node_id=origin_node_id,
        path=[origin_node_id],
        relationships=[],
    )


def impact_analysis(
    node_id: str,
) -> List[str]:
    """
    Return every downstream node affected
    by the supplied node.
    """

    impacted = []

    queue = deque([node_id])

    visited = set()

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        for relationship in uci.outgoing_relationships(current):

            impacted.append(
                relationship.target_node_id
            )

            queue.append(
                relationship.target_node_id
            )

    return impacted


def dependency_chain(
    node_id: str,
) -> List[str]:
    """
    Walk backwards through incoming relationships
    to determine dependency ancestry.
    """

    ancestry = []

    queue = deque([node_id])

    visited = set()

    while queue:

        current = queue.popleft()

        if current in visited:
            continue

        visited.add(current)

        for relationship in uci.incoming_relationships(current):

            ancestry.append(
                relationship.source_node_id
            )

            queue.append(
                relationship.source_node_id
            )

    return ancestry
