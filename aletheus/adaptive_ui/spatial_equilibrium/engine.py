from dataclasses import replace

from .models import *


class Engine:
    def relax(self, node, center_x=0.0, center_y=0.0):
        a = max(0.0, min(1.0, node.priority))
        b = node.bounds
        nb = SpatialBounds(
            b.x + (center_x - b.x) * a * 0.25,
            b.y + (center_y - b.y) * a * 0.25,
            b.z + a * 20,
            b.width * (1 + a * 0.15),
            b.height * (1 + a * 0.15),
            max(1.0, b.depth),
        )
        return replace(node, bounds=nb)
