"""Conservative AST extraction of repository RUF012 candidates."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path


class CandidateClassification(StrEnum):
    """Conservative classification assigned to an extracted candidate."""

    SAFE = "safe"
    UNSAFE = "unsafe"
    UNSUPPORTED = "unsupported"


class MutableValueKind(StrEnum):
    """Mutable class-value syntax recognised by the extractor."""

    LIST = "list"
    DICT = "dict"
    SET = "set"
    LIST_CALL = "list-call"
    DICT_CALL = "dict-call"
    SET_CALL = "set-call"


@dataclass(frozen=True, slots=True)
class ExtractedCandidate:
    """One direct class assignment that may require ClassVar."""

    path: Path
    class_name: str
    attribute_name: str
    line_number: int
    column_offset: int
    classification: CandidateClassification
    value_kind: MutableValueKind
    reason: str

    @property
    def candidate_name(self) -> str:
        """Return a stable class-and-attribute identifier."""

        return f"{self.class_name}.{self.attribute_name}"


@dataclass(frozen=True, slots=True)
class ExtractionFailure:
    """A Python source file that could not be parsed."""

    path: Path
    error: str
    line_number: int | None = None
    column_offset: int | None = None


@dataclass(frozen=True, slots=True)
class FileExtractionResult:
    """AST extraction result for one Python source file."""

    path: Path
    candidates: tuple[ExtractedCandidate, ...]
    failures: tuple[ExtractionFailure, ...] = ()

    @property
    def successful(self) -> bool:
        """Return whether the file parsed without extraction failures."""

        return not self.failures


@dataclass(frozen=True, slots=True)
class RepositoryExtractionResult:
    """Aggregate AST extraction results for multiple Python files."""

    files_processed: int
    candidates: tuple[ExtractedCandidate, ...]
    failures: tuple[ExtractionFailure, ...]

    @property
    def candidates_discovered(self) -> int:
        """Return the number of extracted candidates."""

        return len(self.candidates)

    @property
    def failed_files(self) -> int:
        """Return the number of files that failed parsing."""

        return len({failure.path for failure in self.failures})


class RUF012CandidateExtractor:
    """Extract conservative RUF012 candidates from Python source."""

    _MUTABLE_CALL_NAMES = frozenset({"dict", "list", "set"})

    def extract_file(
        self,
        *,
        path: Path,
        source: str,
    ) -> FileExtractionResult:
        """Extract direct mutable class assignments from one source file."""

        try:
            tree = ast.parse(source, filename=str(path))
        except SyntaxError as exc:
            return FileExtractionResult(
                path=path,
                candidates=(),
                failures=(
                    ExtractionFailure(
                        path=path,
                        error=exc.msg,
                        line_number=exc.lineno,
                        column_offset=exc.offset,
                    ),
                ),
            )

        candidates: list[ExtractedCandidate] = []

        for node in tree.body:
            if not isinstance(node, ast.ClassDef):
                continue

            candidates.extend(
                self._extract_class_candidates(
                    path=path,
                    class_node=node,
                )
            )

        candidates.sort(
            key=lambda candidate: (
                candidate.path.as_posix(),
                candidate.line_number,
                candidate.column_offset,
                candidate.class_name,
                candidate.attribute_name,
            )
        )

        return FileExtractionResult(
            path=path,
            candidates=tuple(candidates),
        )

    def extract_paths(
        self,
        *,
        paths: tuple[Path, ...],
    ) -> RepositoryExtractionResult:
        """Read and extract candidates from deterministic Python paths."""

        candidates: list[ExtractedCandidate] = []
        failures: list[ExtractionFailure] = []

        for path in paths:
            try:
                source = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                failures.append(
                    ExtractionFailure(
                        path=path,
                        error=f"{type(exc).__name__}: {exc}",
                    )
                )
                continue

            result = self.extract_file(
                path=path,
                source=source,
            )
            candidates.extend(result.candidates)
            failures.extend(result.failures)

        candidates.sort(
            key=lambda candidate: (
                candidate.path.as_posix(),
                candidate.line_number,
                candidate.column_offset,
                candidate.class_name,
                candidate.attribute_name,
            )
        )
        failures.sort(
            key=lambda failure: (
                failure.path.as_posix(),
                failure.line_number or 0,
                failure.column_offset or 0,
                failure.error,
            )
        )

        return RepositoryExtractionResult(
            files_processed=len(paths),
            candidates=tuple(candidates),
            failures=tuple(failures),
        )

    def _extract_class_candidates(
        self,
        *,
        path: Path,
        class_node: ast.ClassDef,
    ) -> list[ExtractedCandidate]:
        """Extract candidates from direct statements in one class body."""

        candidates: list[ExtractedCandidate] = []

        for statement in class_node.body:
            candidate = self._candidate_from_statement(
                path=path,
                class_node=class_node,
                statement=statement,
            )

            if candidate is not None:
                candidates.append(candidate)

        return candidates

    def _candidate_from_statement(
        self,
        *,
        path: Path,
        class_node: ast.ClassDef,
        statement: ast.stmt,
    ) -> ExtractedCandidate | None:
        """Build a candidate from one direct class-body statement."""

        if not isinstance(statement, ast.Assign):
            return None

        if len(statement.targets) != 1:
            return None

        target = statement.targets[0]

        if not isinstance(target, ast.Name):
            return None

        value_kind = self._mutable_value_kind(statement.value)

        if value_kind is None:
            return None

        classification, reason = self._classify(
            attribute_name=target.id,
            value=statement.value,
        )

        return ExtractedCandidate(
            path=path,
            class_name=class_node.name,
            attribute_name=target.id,
            line_number=statement.lineno,
            column_offset=statement.col_offset,
            classification=classification,
            value_kind=value_kind,
            reason=reason,
        )

    def _mutable_value_kind(
        self,
        value: ast.expr,
    ) -> MutableValueKind | None:
        """Return the recognised mutable syntax kind for an expression."""

        if isinstance(value, ast.List):
            return MutableValueKind.LIST

        if isinstance(value, ast.Dict):
            return MutableValueKind.DICT

        if isinstance(value, ast.Set):
            return MutableValueKind.SET

        if not isinstance(value, ast.Call):
            return None

        if value.keywords:
            return None

        if not isinstance(value.func, ast.Name):
            return None

        if value.func.id not in self._MUTABLE_CALL_NAMES:
            return None

        if value.func.id == "list":
            return MutableValueKind.LIST_CALL

        if value.func.id == "dict":
            return MutableValueKind.DICT_CALL

        return MutableValueKind.SET_CALL

    def _classify(
        self,
        *,
        attribute_name: str,
        value: ast.expr,
    ) -> tuple[CandidateClassification, str]:
        """Apply conservative safety rules to one mutable assignment."""

        if not attribute_name.isupper():
            return (
                CandidateClassification.UNSAFE,
                "Mutable class attribute is not an uppercase constant.",
            )

        if isinstance(value, (ast.List, ast.Dict, ast.Set)):
            if self._is_literal_container(value):
                return (
                    CandidateClassification.SAFE,
                    (
                        "Uppercase direct class assignment uses "
                        "a literal mutable container."
                    ),
                )

            return (
                CandidateClassification.UNSAFE,
                "Mutable container contains non-literal expressions.",
            )

        if isinstance(value, ast.Call):
            if value.args:
                return (
                    CandidateClassification.UNSAFE,
                    "Mutable constructor call contains positional arguments.",
                )

            return (
                CandidateClassification.SAFE,
                (
                    "Uppercase direct class assignment uses "
                    "an empty mutable constructor."
                ),
            )

        return (
            CandidateClassification.UNSUPPORTED,
            "Mutable expression is not supported by the extractor.",
        )

    def _is_literal_container(
        self,
        value: ast.List | ast.Dict | ast.Set,
    ) -> bool:
        """Return whether a container contains only literal-safe values."""

        try:
            ast.literal_eval(value)
        except (ValueError, TypeError):
            return False

        return True
