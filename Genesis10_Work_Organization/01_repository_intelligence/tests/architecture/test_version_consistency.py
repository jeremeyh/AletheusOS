import tomllib
from pathlib import Path

from aletheus import __version__
from aletheus.runtime import runtime_core

ROOT = Path(__file__).resolve().parents[2]


def test_runtime_uses_canonical_version():
    assert runtime_core.version == __version__


def test_packaging_uses_dynamic_version_source():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert "version" in data["project"]["dynamic"]
    assert data["tool"]["setuptools"]["dynamic"]["version"]["attr"] == "aletheus.version.__version__"


def test_readme_declares_canonical_version():
    first_line = (ROOT / "README.md").read_text().splitlines()[0]
    assert __version__ in first_line
