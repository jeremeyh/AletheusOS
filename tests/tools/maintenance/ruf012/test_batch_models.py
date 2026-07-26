"""Tests for Genesis 11.2 batch-preview result models."""

from pathlib import Path

from tools.maintenance.ruf012.batch_models import (
    BatchItemStatus,
    BatchPreviewItem,
    BatchPreviewSummary,
)


def make_item(
    *,
    status: BatchItemStatus,
    changed: bool = False,
    validated: bool = False,
) -> BatchPreviewItem:
    """Create one representative batch-preview item."""

    return BatchPreviewItem(
        path=Path("package/example.py"),
        class_name="Example",
        attribute_name="VALUES",
        line_number=12,
        classification="safe",
        transformation="ruf012-classvar",
        status=status,
        changed=changed,
        validated=validated,
        notes=("Preview generated.",),
    )


def test_batch_item_exposes_candidate_name() -> None:
    item = make_item(status=BatchItemStatus.VALIDATED)

    assert item.candidate_name == "Example.VALUES"


def test_batch_item_serialises_paths_and_enum_values() -> None:
    item = make_item(
        status=BatchItemStatus.VALIDATED,
        changed=True,
        validated=True,
    )

    payload = item.as_dict()

    assert payload["path"] == "package/example.py"
    assert payload["status"] == "validated"
    assert payload["candidate_name"] == "Example.VALUES"
    assert payload["notes"] == ["Preview generated."]


def test_batch_summary_calculates_status_counts() -> None:
    summary = BatchPreviewSummary(
        repository_root=Path("/repository"),
        files_scanned=20,
        candidates_discovered=4,
        items=(
            make_item(
                status=BatchItemStatus.VALIDATED,
                changed=True,
                validated=True,
            ),
            make_item(status=BatchItemStatus.SKIPPED),
            make_item(status=BatchItemStatus.UNSUPPORTED),
            make_item(status=BatchItemStatus.FAILED),
        ),
    )

    assert summary.validated_count == 1
    assert summary.changed_count == 1
    assert summary.skipped_count == 1
    assert summary.unsupported_count == 1
    assert summary.failed_count == 1
    assert summary.successful is False


def test_batch_summary_is_successful_without_failures_or_writes() -> None:
    summary = BatchPreviewSummary(
        repository_root=Path("/repository"),
        files_scanned=5,
        candidates_discovered=1,
        items=(
            make_item(
                status=BatchItemStatus.VALIDATED,
                changed=True,
                validated=True,
            ),
        ),
        repository_modified=False,
    )

    assert summary.successful is True


def test_batch_summary_serialises_aggregate_values() -> None:
    summary = BatchPreviewSummary(
        repository_root=Path("/repository"),
        files_scanned=5,
        candidates_discovered=1,
        items=(
            make_item(
                status=BatchItemStatus.VALIDATED,
                changed=True,
                validated=True,
            ),
        ),
    )

    payload = summary.as_dict()

    assert payload["repository_root"] == "/repository"
    assert payload["files_scanned"] == 5
    assert payload["candidates_discovered"] == 1
    assert payload["validated"] == 1
    assert payload["changed"] == 1
    assert payload["failed"] == 0
    assert payload["repository_modified"] is False
    assert payload["successful"] is True
