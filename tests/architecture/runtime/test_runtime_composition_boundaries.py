from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
RUNTIME_ROOT = REPOSITORY_ROOT / "aletheus" / "runtime"


def python_sources():
    return tuple(
        path for path in RUNTIME_ROOT.rglob("*.py") if "__pycache__" not in path.parts
    )


def test_legacy_runtime_migration_layers_do_not_return():
    forbidden_paths = (
        RUNTIME_ROOT / "core_shim",
        RUNTIME_ROOT / "core_bridge",
    )

    existing = [
        str(path.relative_to(REPOSITORY_ROOT))
        for path in forbidden_paths
        if path.exists()
    ]

    assert not existing, "Retired runtime migration layers have returned: " + ", ".join(
        existing
    )


def test_no_legacy_runtime_migration_references():
    forbidden_symbols = (
        "RuntimeCoreShim",
        "CoreLifecycleBridge",
        "RuntimeShimReport",
        "CoreLifecycleBridgeReport",
    )

    violations = []

    for path in python_sources():
        source = path.read_text(encoding="utf-8")

        for symbol in forbidden_symbols:
            if symbol in source:
                violations.append(f"{path.relative_to(REPOSITORY_ROOT)}: {symbol}")

    assert not violations, "Legacy runtime migration references remain:\n" + "\n".join(
        sorted(violations)
    )


def test_runtime_kernel_is_constructed_only_by_composition_root():
    allowed_path = RUNTIME_ROOT / "composition" / "root.py"
    violations = []

    for path in python_sources():
        if path == allowed_path:
            continue

        source = path.read_text(encoding="utf-8")

        if "RuntimeKernel(" in source:
            violations.append(str(path.relative_to(REPOSITORY_ROOT)))

    assert not violations, (
        "RuntimeKernel must only be constructed by "
        "aletheus/runtime/composition/root.py:\n" + "\n".join(sorted(violations))
    )


def test_boot_pipeline_has_only_sanctioned_assembly_paths():
    allowed_paths = {
        # Canonical Genesis 11 composition path.
        RUNTIME_ROOT / "composition" / "root.py",
        # Production compatibility path pending completion of
        # RuntimeCore composition integration.
        RUNTIME_ROOT / "core.py",
        # Factory definition.
        RUNTIME_ROOT / "boot_pipeline" / "default_pipeline.py",
    }
    violations = []

    for path in python_sources():
        if path in allowed_paths:
            continue

        source = path.read_text(encoding="utf-8")

        if "build_runtime_boot_pipeline(" in source:
            violations.append(str(path.relative_to(REPOSITORY_ROOT)))

    assert not violations, (
        "The runtime boot pipeline may only be assembled through the "
        "canonical composition root or the explicitly sanctioned "
        "RuntimeCore compatibility path:\\n" + "\\n".join(sorted(violations))
    )


def test_runtime_core_compatibility_boot_path_remains_explicit():
    core_path = RUNTIME_ROOT / "core.py"
    source = core_path.read_text(encoding="utf-8")

    assert "build_runtime_boot_pipeline(" in source, (
        "RuntimeCore no longer directly assembles the boot pipeline. "
        "Review this architecture contract and remove the compatibility "
        "allowance if composition-root integration is complete."
    )
