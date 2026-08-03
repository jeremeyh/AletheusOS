from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "applications" / "constitutional_experience" / "living_frontend"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_phase_names_are_canonical():
    source = read(APP / "src" / "types.ts") + read(
        APP / "src" / "runtime" / "information-physics.ts"
    )
    assert "Quasi-Crystalline" in source
    assert "Quasi-Penrose" not in source

def test_instruments_have_explicit_risk_contract():
    types = read(APP / "src" / "types.ts")
    app = read(APP / "src" / "App.tsx")
    assert "risk: RiskState;" in types
    assert '"stable"' in app
    assert '"watch"' in app
    assert '"strong"' in app

def test_metrology_inventory():
    required = [
        APP / "src" / "runtime" / "quantum-metrology-engine.ts",
        APP / "src" / "runtime" / "magnetic-physics-engine.ts",
        APP / "src" / "hooks" / "useMetrology.ts",
        APP / "src" / "components" / "AdvancedMetrologyPanel.tsx",
    ]
    assert all(path.is_file() for path in required)

def test_spectrum_and_channel_contracts():
    source = read(APP / "src" / "runtime" / "quantum-metrology-engine.ts")
    assert "fftBins: 52" not in source  # configured by the hook, not hard-coded in engine
    hook = read(APP / "src" / "hooks" / "useMetrology.ts")
    assert "fftBins: 52" in hook
    assert "channelCount: 6" in hook

def test_no_render_time_math_random_in_new_metrology():
    paths = [
        APP / "src" / "runtime" / "quantum-metrology-engine.ts",
        APP / "src" / "components" / "AdvancedMetrologyPanel.tsx",
        APP / "src" / "hooks" / "useMetrology.ts",
    ]
    assert all("Math.random" not in read(path) for path in paths)
