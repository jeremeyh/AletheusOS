from __future__ import annotations
from types import SimpleNamespace
from typing import Any
import pytest

@pytest.fixture
def candidate_factory() -> Any:
    def create(
        *,
        path: str = "sample.py",
        class_name: str = "Example",
        attribute_name: str = "VALUES",
        line: int = 2,
        classification: str = "safe-classvar",
    ) -> SimpleNamespace:
        return SimpleNamespace(
            path=path,
            class_name=class_name,
            attribute_name=attribute_name,
            line=line,
            classification=classification,
        )
    return create
