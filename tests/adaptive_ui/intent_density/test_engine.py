from aletheus.adaptive_ui.intent_density.engine import Engine
from aletheus.adaptive_ui.intent_density.models import *

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
    assert (
        Engine().resolve(TelemetryInput(0.2, 0.9, 0.9))
        == DensityLevel.CRITICAL_CRYSTALLINE
    )
