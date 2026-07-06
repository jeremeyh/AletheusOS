from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List


class ExecutiveComponentStatus(str, Enum):
    REGISTERED = "registered"
    READY = "ready"
    FAILED = "failed"
    MISSING_DEPENDENCY = "missing_dependency"


@dataclass(slots=True)
class ExecutiveComponentDescriptor:
    """
    Describes an executive-layer component for composition.

    The descriptor makes architecture explicit and inspectable.
    """

    component_id: str
    name: str
    factory: Callable[[Dict[str, Any]], Any]
    dependencies: List[str] = field(default_factory=list)
    status: ExecutiveComponentStatus = ExecutiveComponentStatus.REGISTERED
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutiveCompositionResult:
    """
    Result of an executive composition pass.
    """

    success: bool
    components: Dict[str, Any]
    order: List[str]
    errors: List[str] = field(default_factory=list)

    def summary(self) -> dict:
        return {
            "success": self.success,
            "component_count": len(self.components),
            "order": self.order,
            "errors": self.errors,
        }


class ExecutiveCompositionEngine:
    """
    Executive Composition Engine

    Responsibilities
    ----------------
    - Register executive component descriptors
    - Validate dependency relationships
    - Resolve build order
    - Construct the executive object graph
    - Return composed components

    It does not execute runtime work.
    It does not mutate runtime/core.py.
    """

    def __init__(self) -> None:
        self._descriptors: Dict[str, ExecutiveComponentDescriptor] = {}

    def register(
        self,
        descriptor: ExecutiveComponentDescriptor,
    ) -> None:
        self._descriptors[descriptor.component_id] = descriptor

    def descriptors(self) -> List[ExecutiveComponentDescriptor]:
        return list(self._descriptors.values())

    def descriptor(
        self,
        component_id: str,
    ) -> ExecutiveComponentDescriptor | None:
        return self._descriptors.get(component_id)

    def dependency_graph(self) -> dict:
        return {
            component_id: list(descriptor.dependencies)
            for component_id, descriptor in self._descriptors.items()
        }

    def validate(self) -> List[str]:
        errors: List[str] = []

        for descriptor in self._descriptors.values():
            for dependency in descriptor.dependencies:
                if dependency not in self._descriptors:
                    errors.append(
                        f"Component '{descriptor.component_id}' depends on "
                        f"missing component '{dependency}'."
                    )

        return errors

    def resolve_order(self) -> tuple[List[str], List[str]]:
        errors = self.validate()

        if errors:
            return [], errors

        resolved: List[str] = []
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(component_id: str) -> None:
            if component_id in visited:
                return

            if component_id in visiting:
                errors.append(
                    f"Circular dependency detected at '{component_id}'."
                )
                return

            visiting.add(component_id)

            descriptor = self._descriptors[component_id]
            for dependency in descriptor.dependencies:
                visit(dependency)

            visiting.remove(component_id)
            visited.add(component_id)

            if component_id not in resolved:
                resolved.append(component_id)

        for component_id in self._descriptors:
            visit(component_id)

        if errors:
            return [], errors

        return resolved, []

    def compose(self) -> ExecutiveCompositionResult:
        order, errors = self.resolve_order()

        if errors:
            return ExecutiveCompositionResult(
                success=False,
                components={},
                order=[],
                errors=errors,
            )

        components: Dict[str, Any] = {}

        for component_id in order:
            descriptor = self._descriptors[component_id]

            try:
                components[component_id] = descriptor.factory(components)
                descriptor.status = ExecutiveComponentStatus.READY

            except Exception as exc:
                descriptor.status = ExecutiveComponentStatus.FAILED
                errors.append(
                    f"Component '{component_id}' failed to compose: {exc}"
                )

        return ExecutiveCompositionResult(
            success=not errors,
            components=components,
            order=order,
            errors=errors,
        )
