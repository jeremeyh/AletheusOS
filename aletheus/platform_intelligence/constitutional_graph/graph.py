"""Authoritative in-memory Constitutional Graph."""

from __future__ import annotations

from collections import Counter, deque
from collections.abc import Iterable
from threading import RLock
from types import MappingProxyType
from uuid import UUID

from aletheus.platform_intelligence.constitutional import (
    ConstitutionalAddress,
    ConstitutionalObject,
    ConstitutionalRelationship,
    RelationshipKind,
)

from .exceptions import (
    ConstitutionalCycleError,
    GraphNodeAlreadyExistsError,
    GraphNodeInUseError,
    GraphNodeNotFoundError,
    GraphRelationshipAlreadyExistsError,
    GraphRelationshipNotFoundError,
)
from .statistics import ConstitutionalGraphStatistics


class ConstitutionalGraph:
    """
    Authoritative topology model for AletheusOS.

    The graph owns constitutional nodes, relationships, traversal, and
    deterministic projections. It does not execute runtime behavior.
    """

    def __init__(
        self,
        *,
        reject_cycles: bool = False,
    ) -> None:
        self._reject_cycles = reject_cycles

        self._nodes: dict[
            ConstitutionalAddress,
            ConstitutionalObject,
        ] = {}

        self._relationships: dict[
            UUID,
            ConstitutionalRelationship,
        ] = {}

        self._outgoing: dict[
            ConstitutionalAddress,
            set[UUID],
        ] = {}

        self._incoming: dict[
            ConstitutionalAddress,
            set[UUID],
        ] = {}

        self._lock = RLock()

    @property
    def reject_cycles(self) -> bool:
        return self._reject_cycles

    def add_node(
        self,
        node: ConstitutionalObject,
    ) -> ConstitutionalObject:
        address = node.identity.address

        with self._lock:
            if address in self._nodes:
                raise GraphNodeAlreadyExistsError(
                    f"Graph node already exists: {address}"
                )

            self._nodes[address] = node
            self._outgoing[address] = set()
            self._incoming[address] = set()

        return node

    def add_nodes(
        self,
        nodes: Iterable[ConstitutionalObject],
    ) -> tuple[ConstitutionalObject, ...]:
        return tuple(
            self.add_node(node)
            for node in nodes
        )

    def update_node(
        self,
        node: ConstitutionalObject,
    ) -> ConstitutionalObject:
        address = node.identity.address

        with self._lock:
            if address not in self._nodes:
                raise GraphNodeNotFoundError(
                    f"Graph node not found: {address}"
                )

            self._nodes[address] = node

        return node

    def get_node(
        self,
        address: str | ConstitutionalAddress,
    ) -> ConstitutionalObject:
        resolved = self._address(address)

        with self._lock:
            node = self._nodes.get(resolved)

        if node is None:
            raise GraphNodeNotFoundError(
                f"Graph node not found: {resolved}"
            )

        return node

    def contains(
        self,
        address: str | ConstitutionalAddress,
    ) -> bool:
        resolved = self._address(address)

        with self._lock:
            return resolved in self._nodes

    def __contains__(
        self,
        address: object,
    ) -> bool:
        if isinstance(address, ConstitutionalAddress):
            return self.contains(address)

        if isinstance(address, str):
            try:
                return self.contains(address)
            except ValueError:
                return False

        return False

    def nodes(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._nodes.values(),
                    key=lambda node: node.address,
                )
            )

    def remove_node(
        self,
        address: str | ConstitutionalAddress,
        *,
        force: bool = False,
    ) -> ConstitutionalObject:
        resolved = self._address(address)
        node = self.get_node(resolved)

        with self._lock:
            connected = (
                self._outgoing[resolved]
                | self._incoming[resolved]
            )

            if connected and not force:
                raise GraphNodeInUseError(
                    f"Graph node {resolved} has "
                    f"{len(connected)} relationships."
                )

            for relationship_id in tuple(connected):
                self._remove_relationship_locked(
                    relationship_id
                )

            del self._nodes[resolved]
            del self._outgoing[resolved]
            del self._incoming[resolved]

        return node

    def add_relationship(
        self,
        relationship: ConstitutionalRelationship,
    ) -> ConstitutionalRelationship:
        source = relationship.source
        target = relationship.target

        with self._lock:
            self._require_node(source)
            self._require_node(target)

            for existing in self._relationships.values():
                if (
                    existing.source == source
                    and existing.target == target
                    and existing.kind == relationship.kind
                ):
                    raise GraphRelationshipAlreadyExistsError(
                        "Equivalent constitutional relationship "
                        "already exists."
                    )

            if (
                self._reject_cycles
                and self._would_create_cycle(
                    source,
                    target,
                )
            ):
                raise ConstitutionalCycleError(
                    f"Relationship {source} -> {target} "
                    "would create a cycle."
                )

            self._relationships[
                relationship.relationship_id
            ] = relationship

            self._outgoing[source].add(
                relationship.relationship_id
            )
            self._incoming[target].add(
                relationship.relationship_id
            )

        return relationship

    def connect(
        self,
        *,
        source: str | ConstitutionalAddress,
        target: str | ConstitutionalAddress,
        kind: RelationshipKind,
        metadata: dict[str, object] | None = None,
    ) -> ConstitutionalRelationship:
        relationship = ConstitutionalRelationship.create(
            source=source,
            target=target,
            kind=kind,
            metadata=metadata,
        )

        return self.add_relationship(relationship)

    def get_relationship(
        self,
        relationship_id: UUID,
    ) -> ConstitutionalRelationship:
        with self._lock:
            relationship = self._relationships.get(
                relationship_id
            )

        if relationship is None:
            raise GraphRelationshipNotFoundError(
                "Graph relationship not found: "
                f"{relationship_id}"
            )

        return relationship

    def remove_relationship(
        self,
        relationship_id: UUID,
    ) -> ConstitutionalRelationship:
        with self._lock:
            return self._remove_relationship_locked(
                relationship_id
            )

    def relationships(
        self,
    ) -> tuple[ConstitutionalRelationship, ...]:
        with self._lock:
            return tuple(
                sorted(
                    self._relationships.values(),
                    key=lambda relationship: (
                        str(relationship.source),
                        str(relationship.target),
                        relationship.kind.value,
                        str(relationship.relationship_id),
                    ),
                )
            )

    def relationships_of(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalRelationship, ...]:
        resolved = self._address(address)
        self.get_node(resolved)

        with self._lock:
            ids = (
                self._outgoing[resolved]
                | self._incoming[resolved]
            )

            return tuple(
                sorted(
                    (
                        self._relationships[item]
                        for item in ids
                    ),
                    key=lambda relationship: (
                        relationship.kind.value,
                        str(relationship.source),
                        str(relationship.target),
                    ),
                )
            )

    def outgoing(
        self,
        address: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalRelationship, ...]:
        resolved = self._address(address)
        self.get_node(resolved)
        kind_filter = frozenset(kinds or ())

        with self._lock:
            relationships = (
                self._relationships[item]
                for item in self._outgoing[resolved]
            )

            return tuple(
                sorted(
                    (
                        relationship
                        for relationship in relationships
                        if (
                            not kind_filter
                            or relationship.kind
                            in kind_filter
                        )
                    ),
                    key=lambda relationship: (
                        relationship.kind.value,
                        str(relationship.target),
                    ),
                )
            )

    def incoming(
        self,
        address: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalRelationship, ...]:
        resolved = self._address(address)
        self.get_node(resolved)
        kind_filter = frozenset(kinds or ())

        with self._lock:
            relationships = (
                self._relationships[item]
                for item in self._incoming[resolved]
            )

            return tuple(
                sorted(
                    (
                        relationship
                        for relationship in relationships
                        if (
                            not kind_filter
                            or relationship.kind
                            in kind_filter
                        )
                    ),
                    key=lambda relationship: (
                        relationship.kind.value,
                        str(relationship.source),
                    ),
                )
            )

    def dependencies(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        return tuple(
            self.get_node(relationship.target)
            for relationship in self.outgoing(
                address,
                kinds={RelationshipKind.DEPENDS_ON},
            )
        )

    def dependents(
        self,
        address: str | ConstitutionalAddress,
    ) -> tuple[ConstitutionalObject, ...]:
        return tuple(
            self.get_node(relationship.source)
            for relationship in self.incoming(
                address,
                kinds={RelationshipKind.DEPENDS_ON},
            )
        )

    def downstream(
        self,
        address: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._traverse(
            address,
            direction="outgoing",
            kinds=kinds,
        )

    def upstream(
        self,
        address: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalObject, ...]:
        return self._traverse(
            address,
            direction="incoming",
            kinds=kinds,
        )

    def shortest_path(
        self,
        source: str | ConstitutionalAddress,
        target: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalObject, ...]:
        source_address = self._address(source)
        target_address = self._address(target)

        self.get_node(source_address)
        self.get_node(target_address)

        if source_address == target_address:
            return (self.get_node(source_address),)

        queue: deque[
            tuple[
                ConstitutionalAddress,
                tuple[ConstitutionalAddress, ...],
            ]
        ] = deque(
            [(source_address, (source_address,))]
        )

        visited = {source_address}

        while queue:
            current, path = queue.popleft()

            for neighbour in self._neighbours(
                current,
                direction="outgoing",
                kinds=kinds,
            ):
                if neighbour in visited:
                    continue

                next_path = path + (neighbour,)

                if neighbour == target_address:
                    return tuple(
                        self.get_node(item)
                        for item in next_path
                    )

                visited.add(neighbour)
                queue.append(
                    (neighbour, next_path)
                )

        return ()

    def is_reachable(
        self,
        source: str | ConstitutionalAddress,
        target: str | ConstitutionalAddress,
        *,
        kinds: set[RelationshipKind] | None = None,
    ) -> bool:
        return bool(
            self.shortest_path(
                source,
                target,
                kinds=kinds,
            )
        )

    def roots(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        with self._lock:
            addresses = (
                address
                for address in self._nodes
                if not self._incoming[address]
            )

            return tuple(
                self._nodes[address]
                for address in sorted(
                    addresses,
                    key=str,
                )
            )

    def leaves(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        with self._lock:
            addresses = (
                address
                for address in self._nodes
                if not self._outgoing[address]
            )

            return tuple(
                self._nodes[address]
                for address in sorted(
                    addresses,
                    key=str,
                )
            )

    def orphans(
        self,
    ) -> tuple[ConstitutionalObject, ...]:
        with self._lock:
            addresses = (
                address
                for address in self._nodes
                if (
                    not self._incoming[address]
                    and not self._outgoing[address]
                )
            )

            return tuple(
                self._nodes[address]
                for address in sorted(
                    addresses,
                    key=str,
                )
            )

    def cycles(
        self,
    ) -> tuple[
        tuple[ConstitutionalAddress, ...],
        ...,
    ]:
        with self._lock:
            addresses = tuple(self._nodes)

        discovered: set[
            tuple[ConstitutionalAddress, ...]
        ] = set()

        for start in addresses:
            self._find_cycles_from(
                start=start,
                current=start,
                path=(start,),
                active={start},
                discovered=discovered,
            )

        return tuple(
            sorted(
                discovered,
                key=lambda cycle: tuple(
                    str(item)
                    for item in cycle
                ),
            )
        )

    def connected_components(
        self,
    ) -> tuple[
        tuple[ConstitutionalObject, ...],
        ...,
    ]:
        with self._lock:
            remaining = set(self._nodes)

        components: list[
            tuple[ConstitutionalObject, ...]
        ] = []

        while remaining:
            start = min(
                remaining,
                key=str,
            )

            queue = deque([start])
            component: set[
                ConstitutionalAddress
            ] = set()

            while queue:
                current = queue.popleft()

                if current in component:
                    continue

                component.add(current)

                neighbours = set(
                    self._neighbours(
                        current,
                        direction="outgoing",
                    )
                )
                neighbours.update(
                    self._neighbours(
                        current,
                        direction="incoming",
                    )
                )

                queue.extend(
                    neighbour
                    for neighbour in neighbours
                    if neighbour not in component
                )

            remaining.difference_update(component)

            components.append(
                tuple(
                    self.get_node(address)
                    for address in sorted(
                        component,
                        key=str,
                    )
                )
            )

        return tuple(
            sorted(
                components,
                key=lambda component: (
                    component[0].address
                    if component
                    else ""
                ),
            )
        )

    def statistics(
        self,
    ) -> ConstitutionalGraphStatistics:
        nodes = self.nodes()
        relationships = self.relationships()
        roots = self.roots()
        leaves = self.leaves()
        orphans = self.orphans()
        cycles = self.cycles()
        components = self.connected_components()

        node_count = len(nodes)
        relationship_count = len(relationships)

        maximum_depth = max(
            (
                len(
                    self.downstream(
                        root.identity.address
                    )
                )
                for root in roots
            ),
            default=0,
        )

        nodes_by_kind = Counter(
            node.kind.value
            for node in nodes
        )
        relationships_by_kind = Counter(
            relationship.kind.value
            for relationship in relationships
        )

        average_degree = (
            relationship_count / node_count
            if node_count
            else 0.0
        )

        return ConstitutionalGraphStatistics(
            nodes=node_count,
            relationships=relationship_count,
            roots=len(roots),
            leaves=len(leaves),
            orphans=len(orphans),
            cycles=len(cycles),
            connected_components=len(components),
            maximum_depth=maximum_depth,
            average_out_degree=average_degree,
            average_in_degree=average_degree,
            nodes_by_kind=MappingProxyType(
                dict(nodes_by_kind)
            ),
            relationships_by_kind=MappingProxyType(
                dict(relationships_by_kind)
            ),
        )

    def snapshot(
        self,
    ) -> dict[str, object]:
        return {
            "nodes": [
                node.to_snapshot()
                for node in self.nodes()
            ],
            "relationships": [
                {
                    "relationship_id": str(
                        relationship.relationship_id
                    ),
                    "source": str(
                        relationship.source
                    ),
                    "target": str(
                        relationship.target
                    ),
                    "kind": relationship.kind.value,
                    "created_at": (
                        relationship.created_at.isoformat()
                    ),
                    "metadata": dict(
                        relationship.metadata
                    ),
                }
                for relationship
                in self.relationships()
            ],
            "topology": {
                "roots": [
                    node.address
                    for node in self.roots()
                ],
                "leaves": [
                    node.address
                    for node in self.leaves()
                ],
                "orphans": [
                    node.address
                    for node in self.orphans()
                ],
                "cycles": [
                    [
                        str(address)
                        for address in cycle
                    ]
                    for cycle in self.cycles()
                ],
                "components": [
                    [
                        node.address
                        for node in component
                    ]
                    for component
                    in self.connected_components()
                ],
            },
            "statistics": self.statistics().to_dict(),
        }

    def _traverse(
        self,
        address: str | ConstitutionalAddress,
        *,
        direction: str,
        kinds: set[RelationshipKind] | None,
    ) -> tuple[ConstitutionalObject, ...]:
        start = self._address(address)
        self.get_node(start)

        queue = deque([start])
        visited = {start}
        ordered: list[ConstitutionalAddress] = []

        while queue:
            current = queue.popleft()

            for neighbour in self._neighbours(
                current,
                direction=direction,
                kinds=kinds,
            ):
                if neighbour in visited:
                    continue

                visited.add(neighbour)
                ordered.append(neighbour)
                queue.append(neighbour)

        return tuple(
            self.get_node(item)
            for item in ordered
        )

    def _neighbours(
        self,
        address: ConstitutionalAddress,
        *,
        direction: str,
        kinds: set[RelationshipKind] | None = None,
    ) -> tuple[ConstitutionalAddress, ...]:
        relationships = (
            self.outgoing(address, kinds=kinds)
            if direction == "outgoing"
            else self.incoming(address, kinds=kinds)
        )

        addresses = (
            relationship.target
            if direction == "outgoing"
            else relationship.source
            for relationship in relationships
        )

        return tuple(
            sorted(
                addresses,
                key=str,
            )
        )

    def _would_create_cycle(
        self,
        source: ConstitutionalAddress,
        target: ConstitutionalAddress,
    ) -> bool:
        if source == target:
            return True

        return self.is_reachable(
            target,
            source,
        )

    def _find_cycles_from(
        self,
        *,
        start: ConstitutionalAddress,
        current: ConstitutionalAddress,
        path: tuple[ConstitutionalAddress, ...],
        active: set[ConstitutionalAddress],
        discovered: set[
            tuple[ConstitutionalAddress, ...]
        ],
    ) -> None:
        for neighbour in self._neighbours(
            current,
            direction="outgoing",
        ):
            if neighbour == start:
                cycle = path
                discovered.add(
                    self._canonical_cycle(cycle)
                )
                continue

            if neighbour in active:
                continue

            self._find_cycles_from(
                start=start,
                current=neighbour,
                path=path + (neighbour,),
                active=active | {neighbour},
                discovered=discovered,
            )

    @staticmethod
    def _canonical_cycle(
        cycle: tuple[ConstitutionalAddress, ...],
    ) -> tuple[ConstitutionalAddress, ...]:
        rotations = [
            cycle[index:] + cycle[:index]
            for index in range(len(cycle))
        ]

        return min(
            rotations,
            key=lambda rotation: tuple(
                str(item)
                for item in rotation
            ),
        )

    def _remove_relationship_locked(
        self,
        relationship_id: UUID,
    ) -> ConstitutionalRelationship:
        relationship = self._relationships.get(
            relationship_id
        )

        if relationship is None:
            raise GraphRelationshipNotFoundError(
                "Graph relationship not found: "
                f"{relationship_id}"
            )

        self._outgoing[
            relationship.source
        ].discard(relationship_id)

        self._incoming[
            relationship.target
        ].discard(relationship_id)

        del self._relationships[
            relationship_id
        ]

        return relationship

    def _require_node(
        self,
        address: ConstitutionalAddress,
    ) -> None:
        if address not in self._nodes:
            raise GraphNodeNotFoundError(
                f"Graph node not found: {address}"
            )

    @staticmethod
    def _address(
        value: str | ConstitutionalAddress,
    ) -> ConstitutionalAddress:
        return (
            value
            if isinstance(value, ConstitutionalAddress)
            else ConstitutionalAddress(value)
        )
