"""Directed acyclic phase graph for TIME™."""

from __future__ import annotations

from collections import defaultdict, deque

from .models import MissionPhaseContract


class DuplicatePhaseError(ValueError):
    pass


class PhaseDependencyError(ValueError):
    pass


class PhaseCycleError(ValueError):
    pass


class MissionPhaseGraph:
    """Canonical DAG of relative mission phases."""

    def __init__(self) -> None:
        self._contracts: dict[
            str,
            MissionPhaseContract,
        ] = {}

    def add(
        self,
        contract: MissionPhaseContract,
    ) -> MissionPhaseContract:
        if contract.phase_id in self._contracts:
            raise DuplicatePhaseError(f"Phase {contract.phase_id!r} already exists.")

        self._contracts[contract.phase_id] = contract
        return contract

    def get(
        self,
        phase_id: str,
    ) -> MissionPhaseContract | None:
        return self._contracts.get(phase_id)

    def require(
        self,
        phase_id: str,
    ) -> MissionPhaseContract:
        contract = self.get(phase_id)

        if contract is None:
            raise KeyError(f"Unknown mission phase: {phase_id}")

        return contract

    def list(
        self,
    ) -> tuple[MissionPhaseContract, ...]:
        return tuple(self._contracts.values())

    def validate(self) -> None:
        known = set(self._contracts)

        for contract in self._contracts.values():
            missing = set(contract.dependencies) - known

            if missing:
                raise PhaseDependencyError(
                    f"Phase {contract.phase_id!r} references "
                    "unknown dependencies: " + ", ".join(sorted(missing))
                )

            if contract.phase_id in contract.dependencies:
                raise PhaseCycleError(f"Phase {contract.phase_id!r} depends on itself.")

        self.ordered()

    def ordered(
        self,
    ) -> tuple[MissionPhaseContract, ...]:
        """
        Return a deterministic topological ordering.

        Raises PhaseCycleError if the graph is not acyclic.
        """

        inbound = {
            phase_id: len(contract.dependencies)
            for phase_id, contract in self._contracts.items()
        }

        dependents: dict[str, list[str]] = defaultdict(list)

        for contract in self._contracts.values():
            for dependency in contract.dependencies:
                dependents[dependency].append(contract.phase_id)

        ready = deque(
            sorted(phase_id for phase_id, count in inbound.items() if count == 0)
        )

        ordered_ids = []

        while ready:
            phase_id = ready.popleft()
            ordered_ids.append(phase_id)

            for dependent in sorted(dependents.get(phase_id, ())):
                inbound[dependent] -= 1

                if inbound[dependent] == 0:
                    ready.append(dependent)

        if len(ordered_ids) != len(self._contracts):
            raise PhaseCycleError("Mission phase graph contains a cycle.")

        return tuple(self._contracts[phase_id] for phase_id in ordered_ids)

    def root_phases(
        self,
    ) -> tuple[MissionPhaseContract, ...]:
        return tuple(
            contract for contract in self.ordered() if not contract.dependencies
        )

    def statistics(self) -> dict:
        return {
            "phases": len(self._contracts),
            "dependencies": sum(
                len(contract.dependencies) for contract in self._contracts.values()
            ),
            "roots": len(self.root_phases()),
        }
