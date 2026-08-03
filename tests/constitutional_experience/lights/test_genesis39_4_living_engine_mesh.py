from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "applications" / "constitutional_experience" / "living_frontend"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_engine_mesh_inventory():
    required = [
        APP / "src/runtime/living-engine-mesh.ts",
        APP / "src/runtime/living-engine-mesh-types.ts",
        APP / "src/runtime/predictive-intent-engine.ts",
        APP / "src/runtime/thermal-field-engine.ts",
        APP / "src/runtime/biological-rhythm-engine.ts",
        APP / "src/runtime/reactive-signal-graph.ts",
        APP / "src/runtime/spatial-layout-boundary.ts",
        APP / "src/runtime/constraint-physics-boundary.ts",
        APP / "src/runtime/sdf-optics-runtime.ts",
        APP / "src/audio/audio-haptic-engine.ts",
        APP / "src/shaders/sdf_amorphous_metallix_39_4.wgsl",
        APP / "src/components/LivingEngineMeshHUD.tsx",
    ]
    assert all(path.is_file() for path in required)

def test_predictive_intent_is_local_and_deterministic():
    source = read(APP / "src/runtime/predictive-intent-engine.ts")
    assert "fetch(" not in source
    assert "Math.random" not in source

def test_engine_mesh_integrates_without_replacing_foundations():
    app = read(APP / "src/App.tsx")
    assert "<LivingEngineMeshHUD" in app
    assert "<HardwareRuntimeHUD" in app
    assert "<REMDreamSubstrate" in app
    assert "<LIGHTSField" in app
    assert "<FounderObservatory" in app

def test_no_malformed_typescript_prefix():
    for path in (APP / "src").rglob("*"):
        if path.suffix in {".ts", ".tsx"}:
            assert not path.read_bytes().startswith(b"\\\n"), path
