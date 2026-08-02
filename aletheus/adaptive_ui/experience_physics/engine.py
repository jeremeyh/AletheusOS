from dataclasses import dataclass

from .models import *


@dataclass(slots=True)
class SpringState:
    current: float
    target: float
    velocity: float = 0.0


class Engine:
    def step(self, s, c, dt):
        dt = min(max(dt, 0.0), 0.032) / 5
        cur = s.current
        vel = s.velocity
        damp = 2 * c.damping_ratio * (c.stiffness * c.mass) ** 0.5
        for _ in range(5):
            force = -c.stiffness * (cur - s.target) - damp * vel
            vel += (force / c.mass) * dt
            cur += vel * dt
        return SpringState(cur, s.target, vel)
