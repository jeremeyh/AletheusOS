"""Tests for conservative RUF012 AST candidate extraction."""

from pathlib import Path

from tools.maintenance.ruf012.extractor import (
    CandidateClassification,
    MutableValueKind,
    RUF012CandidateExtractor,
)


def test_extractor_discovers_uppercase_literal_list() -> None:
    source = '''
class Example:
    VALUES = ["one", "two"]
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert result.successful is True
    assert len(result.candidates) == 1

    candidate = result.candidates[0]

    assert candidate.class_name == "Example"
    assert candidate.attribute_name == "VALUES"
    assert candidate.line_number == 3
    assert candidate.classification == CandidateClassification.SAFE.value
    assert candidate.value_kind is MutableValueKind.LIST


def test_extractor_discovers_literal_dict_and_set() -> None:
    source = '''
class Example:
    MAPPING = {"one": 1}
    NAMES = {"one", "two"}
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert [candidate.attribute_name for candidate in result.candidates] == [
        "MAPPING",
        "NAMES",
    ]
    assert [candidate.value_kind for candidate in result.candidates] == [
        MutableValueKind.DICT,
        MutableValueKind.SET,
    ]
    assert all(
        candidate.classification == CandidateClassification.SAFE.value
        for candidate in result.candidates
    )


def test_extractor_marks_lowercase_mutable_attribute_unsafe() -> None:
    source = '''
class Example:
    values = []
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    candidate = result.candidates[0]

    assert candidate.classification == CandidateClassification.UNSAFE.value
    assert "not an uppercase constant" in candidate.reason


def test_extractor_marks_dynamic_container_unsafe() -> None:
    source = '''
class Example:
    VALUES = [build_value()]
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    candidate = result.candidates[0]

    assert candidate.classification == CandidateClassification.UNSAFE.value
    assert "non-literal expressions" in candidate.reason


def test_extractor_accepts_empty_mutable_constructor_calls() -> None:
    source = '''
class Example:
    ITEMS = list()
    MAPPING = dict()
    NAMES = set()
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert [candidate.value_kind for candidate in result.candidates] == [
        MutableValueKind.LIST_CALL,
        MutableValueKind.DICT_CALL,
        MutableValueKind.SET_CALL,
    ]
    assert all(
        candidate.classification == CandidateClassification.SAFE.value
        for candidate in result.candidates
    )


def test_extractor_marks_constructor_with_arguments_unsafe() -> None:
    source = '''
class Example:
    ITEMS = list(DEFAULT_ITEMS)
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    candidate = result.candidates[0]

    assert candidate.classification == CandidateClassification.UNSAFE.value
    assert "positional arguments" in candidate.reason


def test_extractor_ignores_annotated_assignments() -> None:
    source = '''
from typing import ClassVar

class Example:
    VALUES: ClassVar = []
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert result.candidates == ()


def test_extractor_ignores_instance_assignments() -> None:
    source = '''
class Example:
    def __init__(self) -> None:
        self.values = []
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert result.candidates == ()


def test_extractor_ignores_nested_class_assignments() -> None:
    source = '''
class Outer:
    class Inner:
        VALUES = []
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert result.candidates == ()


def test_extractor_ignores_multiple_target_assignment() -> None:
    source = '''
class Example:
    LEFT = RIGHT = []
'''

    result = RUF012CandidateExtractor().extract_file(
        path=Path("example.py"),
        source=source,
    )

    assert result.candidates == ()


def test_extractor_reports_syntax_errors_without_raising() -> None:
    result = RUF012CandidateExtractor().extract_file(
        path=Path("broken.py"),
        source="class Broken(:\n",
    )

    assert result.successful is False
    assert result.candidates == ()
    assert len(result.failures) == 1
    assert result.failures[0].path == Path("broken.py")
    assert result.failures[0].line_number == 1


def test_extractor_reads_multiple_paths_deterministically(
    tmp_path: Path,
) -> None:
    first = tmp_path / "zeta.py"
    second = tmp_path / "alpha.py"

    first.write_text(
        "class Zeta:\n    VALUES = []\n",
        encoding="utf-8",
    )
    second.write_text(
        "class Alpha:\n    MAPPING = {}\n",
        encoding="utf-8",
    )

    result = RUF012CandidateExtractor().extract_paths(
        paths=(first, second),
    )

    assert result.files_processed == 2
    assert result.candidates_discovered == 2
    assert [candidate.path.name for candidate in result.candidates] == [
        "alpha.py",
        "zeta.py",
    ]
    assert result.failures == ()


def test_extractor_records_unreadable_or_invalid_files(
    tmp_path: Path,
) -> None:
    valid = tmp_path / "valid.py"
    broken = tmp_path / "broken.py"
    missing = tmp_path / "missing.py"

    valid.write_text(
        "class Example:\n    VALUES = []\n",
        encoding="utf-8",
    )
    broken.write_text(
        "class Broken(:\n",
        encoding="utf-8",
    )

    result = RUF012CandidateExtractor().extract_paths(
        paths=(valid, broken, missing),
    )

    assert result.files_processed == 3
    assert result.candidates_discovered == 1
    assert result.failed_files == 2
    assert {failure.path.name for failure in result.failures} == {
        "broken.py",
        "missing.py",
    }
