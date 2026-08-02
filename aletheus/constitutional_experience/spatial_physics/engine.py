from dataclasses import dataclass
from math import sqrt


@dataclass(slots=True)
class Spring:
    position: float = 0.0
    target: float = 0.0
    velocity: float = 0.0
    stiffness: float = 180.0
    damping_ratio: float = 1.0
    mass: float = 1.0


class Engine:
    def step(self, s: Spring, dt: float, substeps: int = 4):
        if s.mass <= 0 or s.stiffness < 0 or substeps < 1:
            raise ValueError("invalid spring")
        h = max(0.0, min(dt, 0.032)) / substeps
        c = 2 * s.damping_ratio * sqrt(s.stiffness * s.mass)
        for _ in range(substeps):
            f = -s.stiffness * (s.position - s.target) - c * s.velocity
            s.velocity += (f / s.mass) * h
            s.position += s.velocity * h
        return s
