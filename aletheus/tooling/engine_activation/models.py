from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class EngineState:
    engine_name: str
    lifecycle: str
    active: bool
    generation: int = 0

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
