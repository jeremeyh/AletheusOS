from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "applications" / "constitutional_experience" / "living_frontend"

def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_source_files_have_no_leading_backslash():
    for path in (APP / "src").rglob("*"):
        if path.suffix in {".ts", ".tsx"}:
            assert not path.read_bytes().startswith(b"\\\n"), path

def test_metrology_hook_is_react_compatible():
    hook = text(APP / "src" / "hooks" / "useMetrology.ts")
    assert "useRef<QuantumMetrologyEngine | null>(null)" in hook
    assert "fftBins: 52" in hook
    assert "channelCount: 6" in hook
    assert "bins:" not in hook
    assert "refreshMs:" not in hook

def test_lights_provider_inventory():
    provider = APP / "src" / "providers" / "LIGHTSProvider.tsx"
    assert provider.is_file()
    source = text(provider)
    assert "phaseForDensity" in source
    assert "constitutionalResonance" in source
    assert "respiration" in source

def test_canonical_phases_remain_locked():
    source = text(APP / "src" / "types.ts")
    assert "Quasi-Crystalline" in source
    assert "Quasi-Penrose" not in source
