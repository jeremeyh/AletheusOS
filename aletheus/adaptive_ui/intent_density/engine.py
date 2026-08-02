from .models import *


class Engine:
    def resolve(self, t):
        t = t.clamped()
        s = (0.5 * t.system_urgency + 0.3 * t.intent_velocity + 0.2 * t.focus_depth) / (
            0.8 * t.cognitive_load + 0.1
        )
        if s > 2 or t.system_urgency > 0.85:
            return DensityLevel.CRITICAL_CRYSTALLINE
        if s > 1.2:
            return DensityLevel.HIGH_DENSITY_FOCUS
        if s > 0.5:
            return DensityLevel.BALANCED
        return DensityLevel.AMBIENT_MINIMAL
