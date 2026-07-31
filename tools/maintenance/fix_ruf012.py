#!/usr/bin/env python3
"""
Genesis 11 - AST RUF012 Analyzer

This version is read-only.

It:
- discovers the repository root,
- scans Python files,
- skips virtual environments, caches, archives, reports, and backups,
- parses files with Python's AST,
- detects mutable class attributes that may trigger Ruff RUF012,
- classifies uppercase constants separately from shared mutable state,
- prints a concise console summary,
- writes Markdown and JSON reports.

It does not modify source files.
"""

from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIR_NAMES = {
    ".git",
    ".github",
    ".idea",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    ".vscode",
    "__pycache__",
    "archives",
    "backups",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "reports",
    "site-packages",
    "venv",
}

SKIP_FILE_SUFFIXES = {
    ".bak",
    ".backup",
    ".orig",
    ".rej",
}

MUTABLE_NODE_TYPES = (
    ast.List,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
)


@dataclass(frozen=True)
class Candidate:
    path: str
    class_name: str
    attribute_name: str
    collection_type: str
    line: int
    column: int
    classification: str
    recommendation: str


@dataclass(frozen=True)
class SyntaxFailure:
    path: str
    line: int | None
    column: int | None
    message: str


@dataclass
class ScanSummary:
    repository: str
    files_discovered: int
    files_parsed: int
    syntax_failures: int
    candidates_found: int
    safe_classvar_candidates: int
    shared_state_candidates: int
    manual_review_candidates: int


@dataclass(frozen=True)
class ScanResult:
    """
    Complete read-only result produced by scan_repository().

    The summary remains separate so existing report functions can continue
    accepting ScanSummary without modification.
    """

    summary: ScanSummary
    candidates: list[Candidate]
    failures: list[SyntaxFailure]
    safe_candidates: list[Candidate]
    shared_candidates: list[Candidate]
    manual_candidates: list[Candidate]

    def __getattr__(self, name: str):
        """
        Delegate summary fields such as files_discovered and files_parsed.

        This preserves a convenient flat result API for package consumers.
        """
        return getattr(self.summary, name)


def find_repo_root(start: Path | None = None) -> Path:
    """
    Locate the repository root.

    Preference order:
    1. nearest parent containing pyproject.toml,
    2. nearest parent containing .git,
    3. current working directory.
    """
    current = (start or Path.cwd()).resolve()

    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file():
            return candidate
        if (candidate / ".git").exists():
            return candidate

    return current


def should_skip(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return True

    if path.suffix != ".py":
        return True

    if any(part in SKIP_DIR_NAMES for part in relative.parts[:-1]):
        return True

    if any(path.name.endswith(suffix) for suffix in SKIP_FILE_SUFFIXES):
        return True

    return False


def iter_python_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*.py"):
        if not should_skip(path, root):
            yield path


def collection_type_name(value: ast.expr) -> str:
    if isinstance(value, ast.List):
        return "list"
    if isinstance(value, ast.Dict):
        return "dict"
    if isinstance(value, ast.Set):
        return "set"
    if isinstance(value, ast.ListComp):
        return "list-comprehension"
    if isinstance(value, ast.DictComp):
        return "dict-comprehension"
    if isinstance(value, ast.SetComp):
        return "set-comprehension"
    return type(value).__name__


def is_uppercase_constant(name: str) -> bool:
    return bool(name) and name.upper() == name and any(char.isalpha() for char in name)


def class_uses_classmethod(class_node: ast.ClassDef) -> bool:
    for statement in class_node.body:
        if not isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        for decorator in statement.decorator_list:
            if isinstance(decorator, ast.Name) and decorator.id == "classmethod":
                return True
            if isinstance(decorator, ast.Attribute) and decorator.attr == "classmethod":
                return True

    return False


def classify_candidate(
    *,
    class_node: ast.ClassDef,
    attribute_name: str,
) -> tuple[str, str]:
    if is_uppercase_constant(attribute_name):
        return (
            "safe-classvar",
            "Annotate as typing.ClassVar with an appropriate collection type.",
        )

    if attribute_name.startswith("_") and class_uses_classmethod(class_node):
        return (
            "shared-class-state",
            "Likely intentional shared state because the class defines classmethods; review before annotating as ClassVar.",
        )

    return (
        "manual-review",
        "Mutable class attribute may be shared unintentionally; inspect usage before changing.",
    )


def extract_assignment_name(statement: ast.stmt) -> tuple[str, ast.expr] | None:
    if isinstance(statement, ast.Assign):
        if len(statement.targets) != 1:
            return None

        target = statement.targets[0]
        if not isinstance(target, ast.Name):
            return None

        return target.id, statement.value

    if isinstance(statement, ast.AnnAssign):
        if not isinstance(statement.target, ast.Name):
            return None

        if statement.value is None:
            return None

        return statement.target.id, statement.value

    return None


def find_candidates(tree: ast.AST, relative_path: str) -> list[Candidate]:
    results: list[Candidate] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef):
            continue

        for statement in node.body:
            extracted = extract_assignment_name(statement)
            if extracted is None:
                continue

            attribute_name, value = extracted

            if not isinstance(value, MUTABLE_NODE_TYPES):
                continue

            classification, recommendation = classify_candidate(
                class_node=node,
                attribute_name=attribute_name,
            )

            results.append(
                Candidate(
                    path=relative_path,
                    class_name=node.name,
                    attribute_name=attribute_name,
                    collection_type=collection_type_name(value),
                    line=getattr(statement, "lineno", 0),
                    column=getattr(statement, "col_offset", 0),
                    classification=classification,
                    recommendation=recommendation,
                )
            )

    return results


def parse_file(
    path: Path,
    root: Path,
) -> tuple[list[Candidate], SyntaxFailure | None]:
    relative_path = path.relative_to(root).as_posix()

    try:
        source = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        return [], SyntaxFailure(
            path=relative_path,
            line=None,
            column=None,
            message=f"UTF-8 decoding failed: {exc}",
        )
    except OSError as exc:
        return [], SyntaxFailure(
            path=relative_path,
            line=None,
            column=None,
            message=f"File read failed: {exc}",
        )

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return [], SyntaxFailure(
            path=relative_path,
            line=exc.lineno,
            column=exc.offset,
            message=exc.msg,
        )

    return find_candidates(tree, relative_path), None


def write_json_report(
    report_path: Path,
    summary: ScanSummary,
    candidates: list[Candidate],
    failures: list[SyntaxFailure],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    payload = {
        "summary": asdict(summary),
        "candidates": [asdict(candidate) for candidate in candidates],
        "syntax_failures": [asdict(failure) for failure in failures],
    }

    report_path.write_text(
        json.dumps(payload, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def write_markdown_report(
    report_path: Path,
    summary: ScanSummary,
    candidates: list[Candidate],
    failures: list[SyntaxFailure],
) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Genesis 11 RUF012 AST Analysis",
        "",
        "## Summary",
        "",
        f"- Repository: `{summary.repository}`",
        f"- Python files discovered: **{summary.files_discovered}**",
        f"- Files parsed successfully: **{summary.files_parsed}**",
        f"- Syntax/read failures: **{summary.syntax_failures}**",
        f"- Mutable class attributes found: **{summary.candidates_found}**",
        f"- Safe `ClassVar` candidates: **{summary.safe_classvar_candidates}**",
        f"- Shared-state candidates: **{summary.shared_state_candidates}**",
        f"- Manual-review candidates: **{summary.manual_review_candidates}**",
        "",
        "## Candidates",
        "",
    ]

    if not candidates:
        lines.append("No mutable class attributes were detected.")
    else:
        lines.extend(
            [
                "| File | Class | Attribute | Type | Line | Classification |",
                "|---|---|---|---:|---:|---|",
            ]
        )

        for candidate in candidates:
            lines.append(
                "| "
                f"`{candidate.path}` | "
                f"`{candidate.class_name}` | "
                f"`{candidate.attribute_name}` | "
                f"`{candidate.collection_type}` | "
                f"{candidate.line} | "
                f"`{candidate.classification}` |"
            )

    lines.extend(["", "## Recommendations", ""])

    for classification in (
        "safe-classvar",
        "shared-class-state",
        "manual-review",
    ):
        matching = [
            candidate
            for candidate in candidates
            if candidate.classification == classification
        ]

        if not matching:
            continue

        lines.append(f"### {classification}")
        lines.append("")

        for candidate in matching:
            lines.append(
                f"- `{candidate.path}:{candidate.line}` "
                f"`{candidate.class_name}.{candidate.attribute_name}` — "
                f"{candidate.recommendation}"
            )

        lines.append("")

    lines.extend(["## Parse Failures", ""])

    if not failures:
        lines.append("No syntax or file-read failures were detected.")
    else:
        for failure in failures:
            location = failure.path
            if failure.line is not None:
                location += f":{failure.line}"
            if failure.column is not None:
                location += f":{failure.column}"

            lines.append(f"- `{location}` — {failure.message}")

    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def print_candidate_group(
    title: str,
    candidates: list[Candidate],
    limit: int,
) -> None:
    print()
    print(title)
    print("-" * len(title))

    if not candidates:
        print("None")
        return

    for candidate in candidates[:limit]:
        print(
            f"{candidate.path}:{candidate.line} "
            f"{candidate.class_name}.{candidate.attribute_name} "
            f"({candidate.collection_type})"
        )

    remaining = len(candidates) - limit
    if remaining > 0:
        print(f"... and {remaining} more")


def scan_repository(
    root: Path,
    *,
    python_files: Iterable[Path] | None = None,
) -> ScanResult:
    """
    Scan a repository for mutable class attributes that may trigger RUF012.

    This function is reusable by both the standalone CLI and the
    tools.maintenance.ruf012 package.

    It performs no writes and produces no console output.
    """
    resolved_root = root.resolve()

    discovered_files = (
        sorted(python_files)
        if python_files is not None
        else sorted(iter_python_files(resolved_root))
    )

    candidates: list[Candidate] = []
    failures: list[SyntaxFailure] = []
    parsed_count = 0

    for path in discovered_files:
        file_candidates, failure = parse_file(path, resolved_root)

        if failure is not None:
            failures.append(failure)
            continue

        parsed_count += 1
        candidates.extend(file_candidates)

    candidates.sort(
        key=lambda item: (
            item.classification,
            item.path,
            item.line,
            item.attribute_name,
        )
    )

    safe_candidates = [
        item for item in candidates if item.classification == "safe-classvar"
    ]

    shared_candidates = [
        item for item in candidates if item.classification == "shared-class-state"
    ]

    manual_candidates = [
        item for item in candidates if item.classification == "manual-review"
    ]

    summary = ScanSummary(
        repository=str(resolved_root),
        files_discovered=len(discovered_files),
        files_parsed=parsed_count,
        syntax_failures=len(failures),
        candidates_found=len(candidates),
        safe_classvar_candidates=len(safe_candidates),
        shared_state_candidates=len(shared_candidates),
        manual_review_candidates=len(manual_candidates),
    )

    return ScanResult(
        summary=summary,
        candidates=candidates,
        failures=failures,
        safe_candidates=safe_candidates,
        shared_candidates=shared_candidates,
        manual_candidates=manual_candidates,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read-only AST analyzer for Ruff RUF012 candidates."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root. Defaults to automatic discovery.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Maximum candidates printed per classification.",
    )
    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Print every detected candidate instead of limiting output.",
    )
    parser.add_argument(
        "--json-report",
        type=Path,
        default=Path("reports/maintenance/ruf012_analysis.json"),
        help="JSON report path, relative to the repository root.",
    )
    parser.add_argument(
        "--markdown-report",
        type=Path,
        default=Path("reports/maintenance/ruf012_analysis.md"),
        help="Markdown report path, relative to the repository root.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    root = find_repo_root(args.root)
    python_files = sorted(iter_python_files(root))

    print("=" * 72)
    print("Genesis 11 - AST RUF012 Analyzer")
    print("=" * 72)
    print()
    print(f"Repository: {root}")
    print(f"Python files discovered: {len(python_files)}")
    print()
    print("Scanning...")

    result = scan_repository(
        root,
        python_files=python_files,
    )

    summary = result.summary
    candidates = result.candidates
    failures = result.failures
    safe_candidates = result.safe_candidates
    shared_candidates = result.shared_candidates
    manual_candidates = result.manual_candidates
    parsed_count = summary.files_parsed

    json_path = (
        args.json_report if args.json_report.is_absolute() else root / args.json_report
    )
    markdown_path = (
        args.markdown_report
        if args.markdown_report.is_absolute()
        else root / args.markdown_report
    )

    write_json_report(json_path, summary, candidates, failures)
    write_markdown_report(markdown_path, summary, candidates, failures)

    print()
    print("Scan complete")
    print("-" * 72)
    print(f"Files parsed successfully: {parsed_count}")
    print(f"Syntax/read failures:       {len(failures)}")
    print(f"Candidates detected:        {len(candidates)}")
    print(f"Safe ClassVar candidates:   {len(safe_candidates)}")
    print(f"Shared-state candidates:    {len(shared_candidates)}")
    print(f"Manual-review candidates:   {len(manual_candidates)}")

    output_limit = len(candidates) if args.include_all else max(args.limit, 0)

    print_candidate_group(
        "Safe ClassVar candidates",
        safe_candidates,
        output_limit,
    )
    print_candidate_group(
        "Shared class-state candidates",
        shared_candidates,
        output_limit,
    )
    print_candidate_group(
        "Manual-review candidates",
        manual_candidates,
        output_limit,
    )

    if failures:
        print()
        print("Parse failures")
        print("--------------")
        for failure in failures[:output_limit]:
            location = failure.path
            if failure.line is not None:
                location += f":{failure.line}"
            if failure.column is not None:
                location += f":{failure.column}"
            print(f"{location}: {failure.message}")

        remaining = len(failures) - output_limit
        if remaining > 0:
            print(f"... and {remaining} more")

    print()
    print(f"JSON report:     {json_path.relative_to(root)}")
    print(f"Markdown report: {markdown_path.relative_to(root)}")
    print()
    print("Read-only analysis complete. No source files were modified.")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
