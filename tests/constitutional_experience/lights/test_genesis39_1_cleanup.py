from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FRONTEND = ROOT / "applications/constitutional_experience/living_frontend"


def test_legacy_components_removed() -> None:
    assert not (FRONTEND / "src/components/AdaptiveField.tsx").exists()
    assert not (FRONTEND / "src/components/InstrumentCard.tsx").exists()


def test_canonical_components_exist() -> None:
    required = (
        "src/components/AxiomCard.tsx",
        "src/components/LIGHTSField.tsx",
        "src/components/FounderObservatory.tsx",
        "src/runtime/lights-engine.ts",
        "src/runtime/information-physics.ts",
        "src/runtime/sight-haptics.ts",
        "src/types.ts",
    )
    for relative in required:
        assert (FRONTEND / relative).exists(), relative


def test_phase_vocabulary_has_no_legacy_name() -> None:
    for source in (FRONTEND / "src").rglob("*"):
        if source.suffix in {".ts", ".tsx", ".css"}:
            assert "Quasi-Crystalline" not in source.read_text(), source


def test_instrument_contract_includes_risk() -> None:
    types = (FRONTEND / "src/types.ts").read_text()
    assert "risk: RiskState;" in types
