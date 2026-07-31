from __future__ import annotations

import ast
from collections.abc import Iterator


def dotted_name(node: ast.AST | None) -> str | None:
    """Return a dotted symbol name for Name and Attribute expressions."""

    if node is None:
        return None

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        parent = dotted_name(node.value)
        if parent:
            return f"{parent}.{node.attr}"
        return node.attr

    if isinstance(node, ast.Call):
        return dotted_name(node.func)

    return None


def final_symbol(name: str | None) -> str | None:
    if not name:
        return None

    return name.rsplit(".", maxsplit=1)[-1]


def iter_names_and_attributes(tree: ast.AST) -> Iterator[ast.Name | ast.Attribute]:
    """Yield top-level symbol references without duplicating attribute segments."""

    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            yield node
            continue

        if isinstance(node, ast.Name):
            yield node
