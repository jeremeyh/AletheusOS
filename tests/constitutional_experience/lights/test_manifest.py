from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
def test_lights_engine(): assert (ROOT/'applications/constitutional_experience/living_frontend/src/runtime/lights-engine.ts').exists()
def test_architecture(): assert (ROOT/'docs/ARCHITECTURE/GENESIS_39_LIGHTS_SIGHT_AXIOMUX_CANONICAL_ARCHITECTURE.md').exists()
