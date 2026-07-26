"""Conservative RUF012 ClassVar transformation."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

from ..utils.candidates import (
    candidate_attribute_name,
    candidate_class_name,
    candidate_classification,
    candidate_line,
)
from .base import Transformation, TransformationError


class ClassVarTransformation(Transformation):
    """Convert one verified class assignment to an unsubscripted ClassVar."""

    name = "ruf012-classvar"

    _SAFE_CLASSIFICATIONS = frozenset(
        {
            "safe",
            "safe-classvar",
            "safe-candidate",
            "safe-rewrite",
        }
    )

    def supports(self, candidate: Any) -> bool:
        """Return whether the candidate is classified as safe."""

        try:
            classification = candidate_classification(candidate)
        except TransformationError:
            return False

        return classification in self._SAFE_CLASSIFICATIONS

    def transform(
        self,
        *,
        candidate: Any,
        path: Path,
        source: str,
    ) -> tuple[str, tuple[str, ...]]:
        """Transform exactly one verified direct class assignment."""

        class_name = candidate_class_name(candidate)
        attribute_name = candidate_attribute_name(candidate)
        line_number = candidate_line(candidate)

        self._verify_ast_target(
            path=path,
            source=source,
            class_name=class_name,
            attribute_name=attribute_name,
            line_number=line_number,
        )

        rewritten = self._annotate_assignment(
            source=source,
            attribute_name=attribute_name,
            line_number=line_number,
        )

        rewritten, import_note = self._ensure_classvar_import(
            rewritten
        )

        return (
            rewritten,
            (
                "Converted direct class assignment to ClassVar.",
                import_note,
            ),
        )

    @staticmethod
    def _verify_ast_target(
        *,
        path: Path,
        source: str,
        class_name: str,
        attribute_name: str,
        line_number: int,
    ) -> None:
        """Verify that the candidate identifies one direct assignment."""

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            raise TransformationError(
                f"Original source is invalid: {exc}"
            ) from exc

        matches: list[ast.Assign] = []

        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            if node.name != class_name:
                continue

            for statement in node.body:
                if not isinstance(statement, ast.Assign):
                    continue

                if statement.lineno != line_number:
                    continue

                if len(statement.targets) != 1:
                    continue

                target = statement.targets[0]

                if (
                    isinstance(target, ast.Name)
                    and target.id == attribute_name
                ):
                    matches.append(statement)

        if len(matches) != 1:
            raise TransformationError(
                "Expected exactly one direct class assignment for "
                f"{class_name}.{attribute_name} on line "
                f"{line_number}; found {len(matches)}."
            )

    @staticmethod
    def _annotate_assignment(
        *,
        source: str,
        attribute_name: str,
        line_number: int,
    ) -> str:
        """Add an unsubscripted ClassVar annotation to the assignment."""

        lines = source.splitlines(keepends=True)
        index = line_number - 1

        if index >= len(lines):
            raise TransformationError(
                f"Candidate line {line_number} is outside the file."
            )

        original_line = lines[index]
        escaped_name = re.escape(attribute_name)

        pattern = re.compile(
            rf"^(?P<indent>[ \t]*)"
            rf"(?P<name>{escaped_name})"
            rf"(?P<spacing>[ \t]*)="
        )

        match = pattern.match(original_line)

        if match is None:
            raise TransformationError(
                "Candidate line is not a simple direct assignment: "
                f"{original_line.rstrip()!r}"
            )

        replacement = (
            f"{match.group('indent')}"
            f"{match.group('name')}: ClassVar"
            f"{match.group('spacing')}="
            f"{original_line[match.end():]}"
        )

        if replacement == original_line:
            raise TransformationError(
                "Transformation produced no assignment change."
            )

        lines[index] = replacement

        return "".join(lines)

    @staticmethod
    def _ensure_classvar_import(
        source: str,
    ) -> tuple[str, str]:
        """Ensure ClassVar is imported from typing."""

        tree = ast.parse(source)
        lines = source.splitlines(keepends=True)

        for statement in tree.body:
            if (
                isinstance(statement, ast.ImportFrom)
                and statement.module == "typing"
                and any(
                    alias.name == "ClassVar"
                    for alias in statement.names
                )
            ):
                return (
                    source,
                    "Existing ClassVar import preserved.",
                )

        for statement in tree.body:
            if not isinstance(statement, ast.ImportFrom):
                continue

            if statement.module != "typing":
                continue

            if statement.lineno != statement.end_lineno:
                continue

            if any(
                alias.name == "*"
                for alias in statement.names
            ):
                continue

            index = statement.lineno - 1
            original_line = lines[index]

            if "#" in original_line or "(" in original_line:
                continue

            newline = (
                "\r\n"
                if original_line.endswith("\r\n")
                else "\n"
                if original_line.endswith("\n")
                else ""
            )

            body = original_line.rstrip("\r\n")
            lines[index] = f"{body}, ClassVar{newline}"

            return (
                "".join(lines),
                "Added ClassVar to existing typing import.",
            )

        insertion_index = (
            ClassVarTransformation._import_insertion_index(tree)
        )

        newline = "\r\n" if "\r\n" in source else "\n"

        lines.insert(
            insertion_index,
            f"from typing import ClassVar{newline}",
        )

        return (
            "".join(lines),
            "Created ClassVar typing import.",
        )

    @staticmethod
    def _import_insertion_index(
        tree: ast.Module,
    ) -> int:
        """Determine where a new typing import should be inserted."""

        insertion_index = 0

        if (
            tree.body
            and isinstance(tree.body[0], ast.Expr)
            and isinstance(tree.body[0].value, ast.Constant)
            and isinstance(tree.body[0].value.value, str)
        ):
            insertion_index = (
                tree.body[0].end_lineno
                or tree.body[0].lineno
            )

        for statement in tree.body:
            if (
                isinstance(statement, ast.ImportFrom)
                and statement.module == "__future__"
            ):
                insertion_index = max(
                    insertion_index,
                    statement.end_lineno
                    or statement.lineno,
                )

        return insertion_index
