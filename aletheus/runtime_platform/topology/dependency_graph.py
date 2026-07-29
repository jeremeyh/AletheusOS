from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, field


class DependencyGraphError(RuntimeError):
    """Base dependency graph error."""


class DependencyCycleError(DependencyGraphError):
    """Raised when a dependency cycle is detected."""


class MissingDependencyError(DependencyGraphError):
    """Raised when a node references an unknown dependency."""


@dataclass(frozen=True, slots=True)
class DependencyNode:
    name: str
    dependencies: tuple[str, ...] = field(default_factory=tuple)


class DependencyGraph:
    """
    Directed acyclic graph used for runtime boot and shutdown ordering.

    An edge A -> B means A depends on B. Therefore B must be started
    before A and stopped after A.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, DependencyNode] = {}

    def add(
        self,
        name: str,
        dependencies: tuple[str, ...] | list[str] = (),
    ) -> DependencyNode:
        normalized = name.strip()

        if not normalized:
            raise ValueError("Dependency node name cannot be empty.")

        node = DependencyNode(
            name=normalized,
            dependencies=tuple(dict.fromkeys(dependencies)),
        )
        self._nodes[normalized] = node
        return node

    def remove(self, name: str) -> bool:
        return self._nodes.pop(name, None) is not None

    def has(self, name: str) -> bool:
        return name in self._nodes

    def get(self, name: str) -> DependencyNode | None:
        return self._nodes.get(name)

    def nodes(self) -> tuple[DependencyNode, ...]:
        return tuple(self._nodes.values())

    def validate(self) -> None:
        missing: dict[str, list[str]] = {}

        for node in self._nodes.values():
            unresolved = [
                dependency
                for dependency in node.dependencies
                if dependency not in self._nodes
            ]

            if unresolved:
                missing[node.name] = unresolved

        if missing:
            raise MissingDependencyError(
                f"Missing dependencies: {missing}"
            )

        self.boot_order()

    def boot_order(self) -> tuple[str, ...]:
        """
        Return dependencies before dependants.
        """

        indegree = {
            name: 0
            for name in self._nodes
        }
        dependants: dict[str, list[str]] = defaultdict(list)

        for node in self._nodes.values():
            for dependency in node.dependencies:
                if dependency not in self._nodes:
                    raise MissingDependencyError(
                        f"{node.name} depends on unknown node "
                        f"{dependency}"
                    )

                indegree[node.name] += 1
                dependants[dependency].append(node.name)

        queue = deque(
            sorted(
                name
                for name, degree in indegree.items()
                if degree == 0
            )
        )

        ordered: list[str] = []

        while queue:
            current = queue.popleft()
            ordered.append(current)

            for dependant in sorted(dependants[current]):
                indegree[dependant] -= 1

                if indegree[dependant] == 0:
                    queue.append(dependant)

        if len(ordered) != len(self._nodes):
            cyclic = sorted(
                name
                for name, degree in indegree.items()
                if degree > 0
            )
            raise DependencyCycleError(
                f"Dependency cycle detected: {cyclic}"
            )

        return tuple(ordered)

    def shutdown_order(self) -> tuple[str, ...]:
        return tuple(reversed(self.boot_order()))

    def dependencies_of(
        self,
        name: str,
        *,
        recursive: bool = False,
    ) -> tuple[str, ...]:
        node = self._nodes.get(name)

        if node is None:
            return ()

        if not recursive:
            return node.dependencies

        resolved: set[str] = set()
        stack = list(node.dependencies)

        while stack:
            dependency = stack.pop()

            if dependency in resolved:
                continue

            resolved.add(dependency)

            dependency_node = self._nodes.get(dependency)

            if dependency_node is not None:
                stack.extend(dependency_node.dependencies)

        return tuple(sorted(resolved))

    def dependants_of(
        self,
        name: str,
        *,
        recursive: bool = False,
    ) -> tuple[str, ...]:
        direct = {
            node.name
            for node in self._nodes.values()
            if name in node.dependencies
        }

        if not recursive:
            return tuple(sorted(direct))

        resolved = set(direct)
        stack = list(direct)

        while stack:
            current = stack.pop()

            for dependant in self.dependants_of(current):
                if dependant not in resolved:
                    resolved.add(dependant)
                    stack.append(dependant)

        return tuple(sorted(resolved))

    def snapshot(self) -> dict[str, object]:
        return {
            "nodes": {
                node.name: list(node.dependencies)
                for node in self._nodes.values()
            },
            "boot_order": list(self.boot_order()),
            "shutdown_order": list(self.shutdown_order()),
        }
