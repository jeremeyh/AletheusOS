"""Transformation registry."""
from __future__ import annotations

from typing import Any

from .transforms import ClassVarTransformation, Transformation


class TransformationRegistry:
    def __init__(self, transformations: tuple[Transformation, ...] | None = None) -> None:
        self._transformations = transformations or (ClassVarTransformation(),)

    @property
    def transformations(self) -> tuple[Transformation, ...]:
        return self._transformations

    def resolve(self, candidate: Any) -> Transformation | None:
        for transformation in self._transformations:
            if transformation.supports(candidate):
                return transformation
        return None
