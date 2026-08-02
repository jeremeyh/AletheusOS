from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

from .helpers import discover_python_files, stable_digest


class Engine:
    VERSION: ClassVar[str] = "36.2.0"
    GENESIS: ClassVar[str] = "36.2"
    CAPABILITY: ClassVar[str] = "Dependency Intelligence"

    def analyze(
        self,
        repository_root: str | Path,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        root = Path(repository_root).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(root)
        files = discover_python_files(root)
        result = {
            "capability": self.CAPABILITY,
            "genesis": self.GENESIS,
            "pythonFileCount": len(files),
            "humanAuthority": "PRESERVED",
            "executionAuthorized": False,
            "context": context or {},
        }
        result["digest"] = stable_digest(result)
        return result
