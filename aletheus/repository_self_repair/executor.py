from __future__ import annotations

import json
import shutil
import tarfile
from datetime import UTC, datetime
from pathlib import Path

from .models import ActionKind, ExecutionResult, RepairPlan
from .scanner import hash_file


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def timestamp() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


class RepairExecutor:
    def execute(
        self,
        plan: RepairPlan,
        *,
        dry_run: bool = True,
        delete_known_orphans: bool = False,
        archive_source: bool = False,
        remove_source: bool = False,
        archive_root: Path | None = None,
    ) -> ExecutionResult:
        started = utc_now()
        target = Path(plan.target_root)
        source = Path(plan.source_root) if plan.source_root else None
        quarantine = target / ".aletheus_restore_points" / "repository_self_repair" / timestamp()
        result = ExecutionResult(started_at=started, completed_at=started, dry_run=dry_run)

        for action in plan.actions:
            try:
                target_path = target / action.relative_path
                if action.kind is ActionKind.COPY:
                    if source is None:
                        raise RuntimeError("copy action without source root")
                    source_path = source / action.relative_path
                    if not dry_run:
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source_path, target_path)
                        actual = hash_file(target_path)
                        if actual != action.source_sha256:
                            raise RuntimeError("post-copy SHA-256 mismatch")
                    result.applied.append({"action": "copy", "path": action.relative_path})
                elif action.kind is ActionKind.QUARANTINE:
                    if not target_path.exists():
                        continue
                    operation = "delete" if delete_known_orphans else "quarantine"
                    if not dry_run:
                        if delete_known_orphans:
                            target_path.unlink()
                        else:
                            destination = quarantine / action.relative_path
                            destination.parent.mkdir(parents=True, exist_ok=True)
                            shutil.move(str(target_path), str(destination))
                    result.applied.append({"action": operation, "path": action.relative_path})
                elif action.kind is ActionKind.CONFLICT:
                    # Preserve target; copy source candidate into review workspace.
                    if source is not None:
                        review = target / ".aletheus_restore_points" / "repository_conflicts" / timestamp() / action.relative_path
                        if not dry_run:
                            review.parent.mkdir(parents=True, exist_ok=True)
                            shutil.copy2(source / action.relative_path, review)
                        result.applied.append({"action": "stage_conflict", "path": action.relative_path, "candidate": str(review)})
            except Exception as exc:  # execution boundary: record and continue
                result.failed.append({"path": action.relative_path, "error": str(exc)})

        if archive_source and source is not None and not result.failed:
            archive_root = (archive_root or target.parent / "repository_archives").resolve()
            archive_path = archive_root / f"{source.name}_{timestamp()}.tar.gz"
            if not dry_run:
                archive_root.mkdir(parents=True, exist_ok=True)
                with tarfile.open(archive_path, "w:gz") as bundle:
                    bundle.add(source, arcname=source.name, recursive=True)
                digest = hash_file(archive_path)
                archive_path.with_suffix(archive_path.suffix + ".sha256").write_text(f"{digest}  {archive_path.name}\n", encoding="utf-8")
                manifest_path = archive_path.with_suffix(archive_path.suffix + ".manifest.json")
                manifest_path.write_text(json.dumps({"source": str(source), "archive": str(archive_path), "sha256": digest, "created_at": utc_now()}, indent=2), encoding="utf-8")
            result.archive_path = str(archive_path)

            if remove_source:
                if not archive_source:
                    result.failed.append({"path": str(source), "error": "source removal requires archive"})
                elif not dry_run:
                    shutil.rmtree(source)
                    result.source_removed = True
                else:
                    result.source_removed = True

        result.completed_at = utc_now()
        return result
