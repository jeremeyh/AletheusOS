from aletheus.adaptive_ui.spatial_equilibrium.engine import Engine
from aletheus.adaptive_ui.spatial_equilibrium.models import *

node = LayoutNode(
    "root",
    "IntentContainer",
    TopologicalState.FLUID_REACTIVE,
    SpatialBounds(0, 0, 0, 100, 100, 10),
    veracity=0.9,
    priority=0.8,
)
scene = LayoutScene("s", DensityLevel.BALANCED, CognitiveState.CALM, node)


def test_engine():
    assert Engine().relax(node).bounds.z > node.bounds.z
