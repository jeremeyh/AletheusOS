from __future__ import annotations

from hashlib import sha256
from json import dumps
from pathlib import Path
from typing import Any


def stable_digest(payload: Any) -> str:
    return sha256(dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def discover_python_files(root: Path) -> list[Path]:
    return sorted(
        p
        for p in root.rglob("*.py")
        if ".venv" not in p.parts
        and ".git" not in p.parts
        and "__pycache__" not in p.parts
    )
