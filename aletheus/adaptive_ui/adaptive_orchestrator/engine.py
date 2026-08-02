from dataclasses import replace

from .models import *


class Engine:
    def orchestrate(self, scene, t):
        t = t.clamped()
        if t.system_urgency >= 0.9:
            cs = CognitiveState.CRITICAL
            d = DensityLevel.CRITICAL_CRYSTALLINE
            topo = TopologicalState.CRYSTALLINE_SOLID
        elif t.cognitive_load >= 0.8:
            cs = CognitiveState.OVERLOADED
            d = DensityLevel.AMBIENT_MINIMAL
            topo = scene.root.topological_state
        elif t.focus_depth >= 0.75:
            cs = CognitiveState.FOCUSED
            d = DensityLevel.HIGH_DENSITY_FOCUS
            topo = (
                TopologicalState.QUASI_CRYSTALLINE
                if scene.root.veracity < 0.98
                else TopologicalState.CRYSTALLINE_SOLID
            )
        else:
            cs = CognitiveState.CALM
            d = DensityLevel.BALANCED
            topo = scene.root.topological_state
        return replace(
            scene,
            density=d,
            cognitive_state=cs,
            root=replace(scene.root, topological_state=topo),
        )
