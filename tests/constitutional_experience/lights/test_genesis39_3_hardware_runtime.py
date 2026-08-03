from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
APP = ROOT / "applications" / "constitutional_experience" / "living_frontend"

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")

def test_hardware_runtime_inventory():
    required = [
        APP / "src/runtime/hardware-capability-detector.ts",
        APP / "src/runtime/adaptive-quality-manager.ts",
        APP / "src/runtime/atomic-ring-buffer.ts",
        APP / "src/runtime/living-experience-hardware-runtime.ts",
        APP / "src/runtime/webgpu-morphogenesis-runtime.ts",
        APP / "src/runtime/use-hardware-runtime.ts",
        APP / "src/components/HardwareRuntimeHUD.tsx",
        APP / "src/workers/kernel-telemetry.worker.ts",
        APP / "src/shaders/rem_morphogenesis_39_3.wgsl",
        ROOT / "runtime/living_experience_kernel/Cargo.toml",
        ROOT / "runtime/living_experience_kernel/src/lib.rs",
    ]
    assert all(path.is_file() for path in required)

def test_no_randomness_in_hardware_runtime():
    paths = [
        APP / "src/runtime/adaptive-quality-manager.ts",
        APP / "src/runtime/living-experience-hardware-runtime.ts",
        APP / "src/runtime/atomic-ring-buffer.ts",
        APP / "src/runtime/webgpu-morphogenesis-runtime.ts",
    ]
    assert all("Math.random" not in read(path) for path in paths)

def test_sab_requires_isolation():
    source = read(APP / "src/runtime/adaptive-quality-manager.ts")
    assert "crossOriginIsolated" in source
    assert "sharedArrayBuffer" in source

def test_app_preserves_rem_and_lights():
    source = read(APP / "src/App.tsx")
    assert "<REMDreamSubstrate" in source
    assert "<LIGHTSField" in source
    assert "<HardwareRuntimeHUD" in source
