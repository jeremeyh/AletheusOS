from dataclasses import dataclass


@dataclass(frozen=True)
class Snapshot:
    name: str
    metrics: dict
