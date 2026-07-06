from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass
class Synapse:
    """
    Neural Synapse™

    Represents a living connection between two neurons.

    Synapses strengthen or weaken over time,
    forming the basis for adaptive cognition.
    """

    id: str

    source: str

    target: str

    purpose: str

    status: str = "inactive"

    strength: float = 0.50

    weight: float = 1.00

    activations: int = 0

    last_fired: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    def fire(self):

        self.activations += 1

        self.last_fired = datetime.now(UTC).isoformat()

        self.strength = min(
            1.0,
            self.strength + 0.002,
        )

    def decay(self):

        self.strength = max(
            0.05,
            self.strength - 0.0005,
        )
