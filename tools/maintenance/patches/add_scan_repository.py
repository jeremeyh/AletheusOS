#!/usr/bin/env python3
"""
One-time refactor for tools/maintenance/fix_ruf012.py.

Adds:
- ScanResult
- scan_repository()

Then rewires main() to consume the reusable scan result.
"""

from __future__ import annotations

import shutil
from pathlib import Path


TARGET = Path("tools/maintenance/fix_ruf012.py")
BACKUP = Path("tools/maintenance/fix_ruf012.py.before_scan_repository.bak")


SCAN_RESULT_MARKER = """
@dataclass(frozen=True)
class ScanResult:
"""


SCAN_RESULT_INSERTION = '''

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
'''


SCAN_FUNCTION = '''

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
        item
        for item in candidates
        if item.classification == "safe-classvar"
    ]

    shared_candidates = [
        item
        for item in candidates
        if item.classification == "shared-class-state"
    ]

    manual_candidates = [
        item
        for item in candidates
        if item.classification == "manual-review"
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
'''


OLD_MAIN_SCAN_BLOCK = """    root = find_repo_root(args.root)
    python_files = sorted(iter_python_files(root))

    candidates: list[Candidate] = []
    failures: list[SyntaxFailure] = []
    parsed_count = 0

    print("=" * 72)
    print("Genesis 11 - AST RUF012 Analyzer")
    print("=" * 72)
    print()
    print(f"Repository: {root}")
    print(f"Python files discovered: {len(python_files)}")
    print()
    print("Scanning...")

    for path in python_files:
        file_candidates, failure = parse_file(path, root)

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
        item
        for item in candidates
        if item.classification == "shared-class-state"
    ]
    manual_candidates = [
        item for item in candidates if item.classification == "manual-review"
    ]

    summary = ScanSummary(
        repository=str(root),
        files_discovered=len(python_files),
        files_parsed=parsed_count,
        syntax_failures=len(failures),
        candidates_found=len(candidates),
        safe_classvar_candidates=len(safe_candidates),
        shared_state_candidates=len(shared_candidates),
        manual_review_candidates=len(manual_candidates),
    )
"""


NEW_MAIN_SCAN_BLOCK = """    root = find_repo_root(args.root)
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
"""


def insert_after_scan_summary(source: str) -> str:
    if SCAN_RESULT_MARKER.strip() in source:
        return source

    anchor = """class ScanSummary:
    repository: str
    files_discovered: int
    files_parsed: int
    syntax_failures: int
    candidates_found: int
    safe_classvar_candidates: int
    shared_state_candidates: int
    manual_review_candidates: int
"""

    if anchor not in source:
        raise RuntimeError(
            "Could not locate the ScanSummary declaration. "
            "The target file may have changed."
        )

    return source.replace(
        anchor,
        anchor + SCAN_RESULT_INSERTION,
        1,
    )


def insert_scan_repository(source: str) -> str:
    if "def scan_repository(" in source:
        return source

    anchor = "\ndef build_parser() -> argparse.ArgumentParser:\n"

    if anchor not in source:
        raise RuntimeError(
            "Could not locate build_parser(). The target file may have changed."
        )

    return source.replace(
        anchor,
        SCAN_FUNCTION + anchor,
        1,
    )


def replace_main_scan_logic(source: str) -> str:
    if OLD_MAIN_SCAN_BLOCK in source:
        return source.replace(
            OLD_MAIN_SCAN_BLOCK,
            NEW_MAIN_SCAN_BLOCK,
            1,
        )

    if "result = scan_repository(" in source:
        return source

    raise RuntimeError(
        "Could not locate the expected scanning block inside main(). "
        "No changes were written."
    )


def main() -> int:
    if not TARGET.is_file():
        raise FileNotFoundError(f"Target file does not exist: {TARGET}")

    original = TARGET.read_text(encoding="utf-8")

    updated = insert_after_scan_summary(original)
    updated = insert_scan_repository(updated)
    updated = replace_main_scan_logic(updated)

    if updated == original:
        print("No changes required. scan_repository() is already installed.")
        return 0

    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
        print(f"Backup created: {BACKUP}")
    else:
        print(f"Backup already exists: {BACKUP}")

    TARGET.write_text(updated, encoding="utf-8")

    print(f"Updated: {TARGET}")
    print("Added ScanResult and scan_repository().")
    print("Rewired main() to use the reusable scanner.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
