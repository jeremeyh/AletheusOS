from dataclasses import replace

from .models import *


class Engine:
    def compile(self, scene, density):
        return replace(scene, density=density, root=self._adapt(scene.root, density))

    def _adapt(self, node, density):
        rank = {
            DensityLevel.AMBIENT_MINIMAL: 0,
            DensityLevel.BALANCED: 1,
            DensityLevel.HIGH_DENSITY_FOCUS: 2,
            DensityLevel.CRITICAL_CRYSTALLINE: 3,
        }
        op = (
            node.opacity
            if rank[density] >= rank[node.behavior.min_density_visibility]
            else 0.0
        )
        return replace(
            node,
            opacity=op,
            children=tuple(self._adapt(c, density) for c in node.children),
        )
