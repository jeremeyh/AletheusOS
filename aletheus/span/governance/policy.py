from dataclasses import dataclass


@dataclass(frozen=True)
class Policy:
    name: str
    category: str
    threshold: float
    comparator: str = ">"
    recommendation: str = ""
