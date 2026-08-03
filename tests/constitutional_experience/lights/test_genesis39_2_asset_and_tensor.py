from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FRONTEND = ROOT / "applications/constitutional_experience/living_frontend"
ASSET = FRONTEND / "public/aletheusos-canonical-mark.jpeg"
EXPECTED_SHA = "945e5bdaf2221dd9ab62ea409919602f0d58333c0fd7af18377895f4c69db631"


def test_canonical_logo_asset_exists() -> None:
    assert ASSET.exists()


def test_canonical_logo_hash() -> None:
    assert sha256(ASSET.read_bytes()).hexdigest() == EXPECTED_SHA


def test_wrong_screenshot_asset_removed() -> None:
    assert not (
        FRONTEND / "public/aletheusos-principle-x.png"
    ).exists()


def test_tensor_runtime_exists() -> None:
    assert (
        FRONTEND / "src/runtime/tensor-field.ts"
    ).exists()


def test_all_logo_references_are_canonical() -> None:
    for path in (FRONTEND / "src").rglob("*"):
        if path.suffix in {".ts", ".tsx", ".css"}:
            text = path.read_text()
            assert "aletheusos-principle-x.png" not in text
