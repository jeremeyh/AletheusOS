"""Constitutional Dependency Manager."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Iterable

from aletheus.platform_intelligence.service_registry import (
    PlatformServiceRegistry,
)

from .exceptions import (
    DependencyCycleError,
    DependencyNodeNotFoundError,
    MissingDependencyError,
)
from .models import (
    ConstitutionalDependencyPlan,
    DependencyLevel,
    DependencyManagerStatistics,
    DependencyValidation,
)


class ConstitutionalDependencyManager:
    """
    Pure dependency-planning layer for Platform Intelligence.

    CDM validates service dependencies and produces immutable boot, shutdown,
    and restart plans. It never starts, stops, transitions, publishes, or
    mutates runtime services.
    """

    def __init__(
        self,
        *,
        service_registry: PlatformServiceRegistry,
    ) -> None:
        self._service_registry = service_registry

    def validate(self) -> DependencyValidation:
        services = self._service_registry.all()
        addresses = {
            service.address
            for service in services
        }

        missing: dict[
            str,
            tuple[str, ...],
        ] = {}
        self_dependencies: list[str] = []
        edges = 0

        for service in services:
            dependencies = tuple(
                sorted(
                    self._service_dependencies(
                        service
                    )
                )
            )
            edges += len(dependencies)

            unresolved = tuple(
                dependency
                for dependency in dependencies
                if dependency not in addresses
            )

            if unresolved:
                missing[service.address] = (
                    unresolved
                )

            if service.address in dependencies:
                self_dependencies.append(
                    service.address
                )

        cycles = self._find_cycles()

        return DependencyValidation(
            valid=(
                not missing
                and not self_dependencies
                and not cycles
            ),
            registered_services=len(services),
            dependency_edges=edges,
            missing_dependencies=missing,
            cycles=cycles,
            self_dependencies=tuple(
                sorted(self_dependencies)
            ),
        )

    def build_boot_plan(
        self,
    ) -> ConstitutionalDependencyPlan:
        validation = self.validate()

        if validation.missing_dependencies:
            raise MissingDependencyError(
                "Cannot build boot plan with "
                "missing dependencies."
            )

        if validation.self_dependencies:
            raise DependencyCycleError(
                "Cannot build boot plan with "
                "self-dependencies."
            )

        if validation.cycles:
            raise DependencyCycleError(
                "Cannot build boot plan with "
                "dependency cycles."
            )

        dependencies = self._dependency_map()
        dependents = self._dependent_map(
            dependencies
        )

        unresolved_count = {
            address: len(values)
            for address, values
            in dependencies.items()
        }

        ready = sorted(
            address
            for address, count
            in unresolved_count.items()
            if count == 0
        )

        levels: list[DependencyLevel] = []
        processed: set[str] = set()
        level_index = 0

        while ready:
            current = tuple(ready)

            levels.append(
                DependencyLevel(
                    index=level_index,
                    services=current,
                )
            )

            next_ready: list[str] = []

            for address in current:
                processed.add(address)

                for dependent in sorted(
                    dependents[address]
                ):
                    unresolved_count[
                        dependent
                    ] -= 1

                    if (
                        unresolved_count[
                            dependent
                        ]
                        == 0
                    ):
                        next_ready.append(
                            dependent
                        )

            ready = sorted(set(next_ready))
            level_index += 1

        if len(processed) != len(dependencies):
            raise DependencyCycleError(
                "Dependency graph could not be "
                "topologically resolved."
            )

        return ConstitutionalDependencyPlan.create(
            direction="boot",
            levels=tuple(levels),
            dependency_edges=(
                validation.dependency_edges
            ),
        )

    def build_shutdown_plan(
        self,
    ) -> ConstitutionalDependencyPlan:
        boot = self.build_boot_plan()

        reversed_levels = tuple(
            DependencyLevel(
                index=index,
                services=level.services,
            )
            for index, level in enumerate(
                reversed(boot.levels)
            )
        )

        return ConstitutionalDependencyPlan.create(
            direction="shutdown",
            levels=reversed_levels,
            dependency_edges=(
                boot.dependency_edges
            ),
        )

    def build_restart_plan(
        self,
        address: str,
    ) -> ConstitutionalDependencyPlan:
        resolved = address.strip().lower()
        dependencies = self._dependency_map()

        if resolved not in dependencies:
            raise DependencyNodeNotFoundError(
                f"Service not found: {resolved}"
            )

        dependents = self._dependent_map(
            dependencies
        )

        affected = self._collect_dependents(
            resolved,
            dependents,
        )
        affected.add(resolved)

        boot = self.build_boot_plan()

        selected_levels = tuple(
            DependencyLevel(
                index=index,
                services=tuple(
                    service
                    for service in level.services
                    if service in affected
                ),
            )
            for index, level in enumerate(
                level
                for level in boot.levels
                if any(
                    service in affected
                    for service
                    in level.services
                )
            )
        )

        edge_count = sum(
            1
            for service in affected
            for dependency
            in dependencies[service]
            if dependency in affected
        )

        return ConstitutionalDependencyPlan.create(
            direction="restart",
            levels=selected_levels,
            dependency_edges=edge_count,
        )

    def dependencies_of(
        self,
        address: str,
        *,
        transitive: bool = False,
    ) -> tuple[str, ...]:
        resolved = address.strip().lower()
        dependencies = self._dependency_map()

        if resolved not in dependencies:
            raise DependencyNodeNotFoundError(
                f"Service not found: {resolved}"
            )

        if not transitive:
            return tuple(
                sorted(dependencies[resolved])
            )

        return tuple(
            sorted(
                self._collect_dependencies(
                    resolved,
                    dependencies,
                )
            )
        )

    def dependents_of(
        self,
        address: str,
        *,
        transitive: bool = False,
    ) -> tuple[str, ...]:
        resolved = address.strip().lower()
        dependencies = self._dependency_map()

        if resolved not in dependencies:
            raise DependencyNodeNotFoundError(
                f"Service not found: {resolved}"
            )

        dependents = self._dependent_map(
            dependencies
        )

        if not transitive:
            return tuple(
                sorted(dependents[resolved])
            )

        return tuple(
            sorted(
                self._collect_dependents(
                    resolved,
                    dependents,
                )
            )
        )

    def statistics(
        self,
    ) -> DependencyManagerStatistics:
        plan = self.build_boot_plan()
        dependencies = self._dependency_map()
        dependents = self._dependent_map(
            dependencies
        )

        return DependencyManagerStatistics(
            services=len(dependencies),
            dependency_edges=(
                plan.dependency_edges
            ),
            boot_levels=len(plan.levels),
            maximum_depth=plan.maximum_depth,
            parallel_groups=(
                plan.parallel_groups
            ),
            root_services=sum(
                not values
                for values in dependencies.values()
            ),
            leaf_services=sum(
                not values
                for values in dependents.values()
            ),
        )

    def export(self) -> dict[str, object]:
        validation = self.validate()

        payload: dict[str, object] = {
            "validation": validation.to_dict(),
        }

        if validation.valid:
            payload["boot_plan"] = (
                self.build_boot_plan().to_dict()
            )
            payload["shutdown_plan"] = (
                self.build_shutdown_plan().to_dict()
            )
            payload["statistics"] = (
                self.statistics().to_dict()
            )

        return payload

    def _dependency_map(
        self,
    ) -> dict[str, set[str]]:
        return {
            service.address: set(
                self._service_dependencies(
                    service
                )
            )
            for service
            in self._service_registry.all()
        }

    @staticmethod
    def _service_dependencies(
        service,
    ) -> tuple[str, ...]:
        raw_dependencies = (
            service.attributes.get(
                "dependencies",
                (),
            )
        )

        if raw_dependencies is None:
            return ()

        if isinstance(
            raw_dependencies,
            str,
        ):
            normalized = (
                raw_dependencies.strip().lower()
            )

            return (
                (normalized,)
                if normalized
                else ()
            )

        try:
            values = tuple(
                dependency.strip().lower()
                for dependency
                in raw_dependencies
                if isinstance(
                    dependency,
                    str,
                )
                and dependency.strip()
            )
        except TypeError as error:
            raise TypeError(
                "Service dependency attributes must "
                "be a string or iterable of strings."
            ) from error

        return tuple(
            sorted(set(values))
        )

    @staticmethod
    def _dependent_map(
        dependencies: dict[str, set[str]],
    ) -> dict[str, set[str]]:
        dependents = {
            address: set()
            for address in dependencies
        }

        for address, values in (
            dependencies.items()
        ):
            for dependency in values:
                if dependency in dependents:
                    dependents[
                        dependency
                    ].add(address)

        return dependents

    def _find_cycles(
        self,
    ) -> tuple[tuple[str, ...], ...]:
        graph = self._dependency_map()
        visiting: set[str] = set()
        visited: set[str] = set()
        stack: list[str] = []
        cycles: set[tuple[str, ...]] = set()

        def visit(address: str) -> None:
            if address in visited:
                return

            if address in visiting:
                start = stack.index(address)
                cycle = tuple(
                    stack[start:] + [address]
                )
                cycles.add(
                    self._normalize_cycle(cycle)
                )
                return

            visiting.add(address)
            stack.append(address)

            for dependency in sorted(
                graph.get(address, ())
            ):
                if dependency in graph:
                    visit(dependency)

            stack.pop()
            visiting.remove(address)
            visited.add(address)

        for address in sorted(graph):
            visit(address)

        return tuple(sorted(cycles))

    @staticmethod
    def _normalize_cycle(
        cycle: tuple[str, ...],
    ) -> tuple[str, ...]:
        values = list(cycle[:-1])

        if not values:
            return cycle

        rotations = [
            tuple(
                values[index:]
                + values[:index]
            )
            for index in range(len(values))
        ]

        normalized = min(rotations)

        return normalized + (normalized[0],)

    @staticmethod
    def _collect_dependencies(
        address: str,
        dependencies: dict[str, set[str]],
    ) -> set[str]:
        collected: set[str] = set()
        queue = deque(
            dependencies[address]
        )

        while queue:
            current = queue.popleft()

            if current in collected:
                continue

            collected.add(current)

            queue.extend(
                dependencies.get(current, ())
            )

        return collected

    @staticmethod
    def _collect_dependents(
        address: str,
        dependents: dict[str, set[str]],
    ) -> set[str]:
        collected: set[str] = set()
        queue = deque(
            dependents[address]
        )

        while queue:
            current = queue.popleft()

            if current in collected:
                continue

            collected.add(current)

            queue.extend(
                dependents.get(current, ())
            )

        return collected
