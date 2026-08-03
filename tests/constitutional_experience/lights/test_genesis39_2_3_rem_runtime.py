from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "applications" / "constitutional_experience" / "living_frontend"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_rem_runtime_inventory():
    required = [
        APP / "src/runtime/rem-types.ts",
        APP / "src/runtime/rem-runtime.ts",
        APP / "src/runtime/morphogenesis-engine.ts",
        APP / "src/runtime/temporal-determinism-monitor.ts",
        APP / "src/runtime/deterministic-noise.ts",
        APP / "src/components/REMDreamSubstrate.tsx",
        APP / "src/components/REMRuntimeHUD.tsx",
        APP / "src/shaders/rem-particle-compute.wgsl",
        APP / "src/workers/rem-runtime.worker.ts",
        APP / "src/wasm/rem_kernel.rs",
    ]
    assert all(path.is_file() for path in required)

def test_rem_runtime_is_deterministic():
    runtime = read(APP / "src/runtime/rem-runtime.ts")
    component = read(APP / "src/components/REMDreamSubstrate.tsx")
    assert "Math.random" not in runtime
    assert "Math.random" not in component
    assert "DeterministicNoise" in runtime

def test_morphogenesis_lifecycle():
    source = read(APP / "src/runtime/rem-types.ts")
    for phase in [
        "ambient", "nucleating", "condensing",
        "stabilized", "transforming", "dissolving",
    ]:
        assert f'"{phase}"' in source

def test_app_integrates_rem_without_replacing_lights():
    app = read(APP / "src/App.tsx")
    assert "<REMDreamSubstrate" in app
    assert "<LIGHTSField" in app
    assert "<AdvancedMetrologyPanel" in app
    assert "<FounderObservatory" in app

def test_no_malformed_source_prefix():
    for path in (APP / "src").rglob("*"):
        if path.suffix in {".ts", ".tsx"}:
            assert not path.read_bytes().startswith(b"\\\n"), path
