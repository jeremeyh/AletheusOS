from pathlib import Path

from aletheus.repository_self_repair import RepositorySelfRepairEngine
from aletheus.repository_self_repair.models import ActionKind


def test_plans_copy_conflict_and_orphan(tmp_path: Path) -> None:
    target = tmp_path / "target"
    source = tmp_path / "source"
    target.mkdir()
    source.mkdir()
    (target / "same.py").write_text("same", encoding="utf-8")
    (source / "same.py").write_text("same", encoding="utf-8")
    (target / "different.py").write_text("target", encoding="utf-8")
    (source / "different.py").write_text("source", encoding="utf-8")
    (source / "new.py").write_text("new", encoding="utf-8")
    (target / "=END").write_text("", encoding="utf-8")

    _, _, plan = RepositorySelfRepairEngine().diagnose(target, source)
    kinds = {a.relative_path: a.kind for a in plan.actions}
    assert kinds["same.py"] is ActionKind.KEEP
    assert kinds["different.py"] is ActionKind.CONFLICT
    assert kinds["new.py"] is ActionKind.COPY
    assert kinds["=END"] is ActionKind.QUARANTINE


def test_apply_copies_and_quarantines_without_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "target"
    source = tmp_path / "source"
    target.mkdir()
    source.mkdir()
    (target / "different.py").write_text("target", encoding="utf-8")
    (source / "different.py").write_text("source", encoding="utf-8")
    (source / "new.py").write_text("new", encoding="utf-8")
    (target / "=END").write_text("", encoding="utf-8")

    _, result, report = RepositorySelfRepairEngine().run(target, source, apply=True)
    assert result.success
    assert (target / "new.py").read_text(encoding="utf-8") == "new"
    assert (target / "different.py").read_text(encoding="utf-8") == "target"
    assert not (target / "=END").exists()
    assert report.exists()
    candidates = list(
        (target / ".aletheus_restore_points" / "repository_conflicts").rglob(
            "different.py"
        )
    )
    assert candidates and candidates[0].read_text(encoding="utf-8") == "source"


def test_source_removal_requires_verified_archive(tmp_path: Path) -> None:
    target = tmp_path / "target"
    source = tmp_path / "source"
    target.mkdir()
    source.mkdir()
    (source / "new.py").write_text("new", encoding="utf-8")

    _, result, _ = RepositorySelfRepairEngine().run(
        target,
        source,
        apply=True,
        archive_source=True,
        remove_source=True,
        archive_root=tmp_path / "archives",
    )
    assert result.success
    assert result.archive_path
    assert Path(result.archive_path).exists()
    assert Path(result.archive_path + ".sha256").exists()
    assert not source.exists()
