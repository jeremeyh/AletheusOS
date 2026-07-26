"""Candidate attribute access helpers."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ..transforms.base import TransformationError


def candidate_value(candidate: Any, *names: str, required: bool = True) -> Any:
    for name in names:
        if hasattr(candidate, name):
            value = getattr(candidate, name)
            if value is not None:
                return value
    if required:
        raise TransformationError("Candidate is missing a required attribute: " + ", ".join(names) + ".")
    return None

def candidate_path(candidate: Any) -> Path:
    value = candidate_value(candidate, "path", "file_path", "filename")
    if not isinstance(value, (str, Path)):
        raise TransformationError("Candidate path must be a string or pathlib.Path.")
    return Path(value)

def candidate_class_name(candidate: Any) -> str:
    value = candidate_value(candidate, "class_name", "className")
    if not isinstance(value, str) or not value:
        raise TransformationError("Candidate class name must be a non-empty string.")
    return value

def candidate_attribute_name(candidate: Any) -> str:
    value = candidate_value(candidate, "attribute_name", "name", "variable_name", "target_name")
    if not isinstance(value, str) or not value:
        raise TransformationError("Candidate attribute name must be a non-empty string.")
    return value

def candidate_line(candidate: Any) -> int:
    value = candidate_value(candidate, "line", "line_number", "lineno")
    if not isinstance(value, int) or value < 1:
        raise TransformationError("Candidate line must be a positive integer.")
    return value

def candidate_classification(candidate: Any) -> str:
    value = candidate_value(candidate, "classification", "category", required=False)
    if value is None:
        return "safe-classvar"
    if hasattr(value, "value"):
        value = value.value
    return str(value).strip().lower().replace("_", "-")
