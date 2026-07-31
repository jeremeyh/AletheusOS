"""Canonical lifecycle transition policy for AletheusOS."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import AbstractSet

from .enums import ConstitutionalState
from .exceptions import ConstitutionalTransitionError

_CANONICAL_TRANSITIONS: Mapping[
    ConstitutionalState,
    frozenset[ConstitutionalState],
] = MappingProxyType(
    {
        ConstitutionalState.REGISTERED: frozenset(
            {
                ConstitutionalState.INITIALIZING,
                ConstitutionalState.RETIRED,
            }
        ),
        ConstitutionalState.INITIALIZING: frozenset(
            {
                ConstitutionalState.STARTING,
                ConstitutionalState.DEGRADED,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.STARTING: frozenset(
            {
                ConstitutionalState.RUNNING,
                ConstitutionalState.DEGRADED,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.RUNNING: frozenset(
            {
                ConstitutionalState.PAUSED,
                ConstitutionalState.DEGRADED,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.PAUSED: frozenset(
            {
                ConstitutionalState.RUNNING,
                ConstitutionalState.DEGRADED,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.DEGRADED: frozenset(
            {
                ConstitutionalState.RECOVERING,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.RECOVERING: frozenset(
            {
                ConstitutionalState.RUNNING,
                ConstitutionalState.DEGRADED,
                ConstitutionalState.STOPPING,
            }
        ),
        ConstitutionalState.STOPPING: frozenset(
            {
                ConstitutionalState.STOPPED,
                ConstitutionalState.DEGRADED,
            }
        ),
        ConstitutionalState.STOPPED: frozenset(
            {
                ConstitutionalState.STARTING,
                ConstitutionalState.RETIRED,
            }
        ),
        ConstitutionalState.RETIRED: frozenset(),
    }
)


@dataclass(frozen=True, slots=True)
class ConstitutionalTransitionPolicy:
    """
    Authoritative lifecycle transition policy.

    The policy is immutable and shared across runtime services, registries,
    applications, graph projections, and the Platform Digital Twin.
    """

    transitions: Mapping[
        ConstitutionalState,
        AbstractSet[ConstitutionalState],
    ]

    @classmethod
    def canonical(cls) -> ConstitutionalTransitionPolicy:
        return cls(transitions=_CANONICAL_TRANSITIONS)

    def allowed_targets(
        self,
        current_state: ConstitutionalState,
    ) -> frozenset[ConstitutionalState]:
        targets = self.transitions.get(current_state)

        if targets is None:
            return frozenset()

        return frozenset(targets)

    def permits(
        self,
        current_state: ConstitutionalState,
        target_state: ConstitutionalState,
    ) -> bool:
        return target_state in self.allowed_targets(current_state)

    def require(
        self,
        current_state: ConstitutionalState,
        target_state: ConstitutionalState,
    ) -> None:
        if current_state == target_state:
            raise ConstitutionalTransitionError(
                current_state,
                target_state,
                reason="A lifecycle transition must change state.",
            )

        if not self.permits(current_state, target_state):
            allowed = sorted(
                state.value for state in self.allowed_targets(current_state)
            )

            raise ConstitutionalTransitionError(
                current_state,
                target_state,
                reason=(
                    f"Allowed targets from {current_state.value}: "
                    f"{', '.join(allowed) if allowed else 'none'}"
                ),
            )


CANONICAL_TRANSITION_POLICY = ConstitutionalTransitionPolicy.canonical()
