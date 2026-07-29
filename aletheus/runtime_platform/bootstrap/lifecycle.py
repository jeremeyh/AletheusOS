from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from .boot_phase import BootPhase


@dataclass(slots=True)
class BootStep:
    phase: BootPhase
    action: Callable
    description: str = ""


class RuntimeLifecycle:
    """
    Ordered runtime boot pipeline.

    The lifecycle owns phase ordering only.
    It performs no runtime composition itself.
    """

    def __init__(self) -> None:
        self._steps: list[BootStep] = []

    def add(
        self,
        phase: BootPhase,
        action: Callable,
        description: str = "",
    ) -> None:
        self._steps.append(
            BootStep(
                phase=phase,
                action=action,
                description=description,
            )
        )

    @property
    def steps(self) -> tuple[BootStep, ...]:
        return tuple(self._steps)
