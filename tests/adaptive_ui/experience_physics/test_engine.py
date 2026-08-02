from aletheus.adaptive_ui.experience_physics.engine import Engine, SpringState
from aletheus.adaptive_ui.experience_physics.models import *

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
    assert Engine().step(SpringState(0, 1), PhysicsConfig(), 0.016).current > 0
