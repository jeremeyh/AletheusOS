from dataclasses import dataclass


@dataclass(frozen=True)
class FitnessResult:
    name: str
    score: float
    passed: bool
    observed: float
    target: float
