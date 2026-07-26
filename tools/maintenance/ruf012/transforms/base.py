"""Base transformation interfaces."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class TransformationError(RuntimeError):
    pass

class Transformation(ABC):
    name: str

    @abstractmethod
    def supports(self, candidate: Any) -> bool:
        raise NotImplementedError

    @abstractmethod
    def transform(self, *, candidate: Any, path: Path, source: str) -> tuple[str, tuple[str, ...]]:
        raise NotImplementedError
