from __future__ import annotations

from datetime import UTC, datetime

from .models import Action, ActionKind, FileClass, RepairPlan, ScanManifest
from .policy import RepairPolicy


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class RepairPlanner:
    def __init__(self, policy: RepairPolicy) -> None:
        self.policy = policy

    def plan(self, target: ScanManifest, source: ScanManifest | None = None) -> RepairPlan:
        plan = RepairPlan(
            source_root=source.root if source else None,
            target_root=target.root,
            generated_at=utc_now(),
        )
        target_paths = set(target.records)
        source_paths = set(source.records) if source else set()

        for path in sorted(target_paths | source_paths):
            target_record = target.records.get(path)
            source_record = source.records.get(path) if source else None

            if target_record and self.policy.is_known_orphan(path, target_record.size):
                plan.actions.append(Action(ActionKind.QUARANTINE, path, "known orphan/debris rule", target_sha256=target_record.sha256))
                continue

            if source_record and not target_record:
                if source_record.file_class in {FileClass.CACHE, FileClass.GENERATED}:
                    plan.actions.append(Action(ActionKind.SKIP, path, f"source-only {source_record.file_class.value}"))
                elif self.policy.is_known_orphan(path, source_record.size):
                    plan.actions.append(Action(ActionKind.SKIP, path, "source-only known orphan"))
                else:
                    plan.actions.append(Action(ActionKind.COPY, path, "exists only in source", source_sha256=source_record.sha256))
                continue

            if target_record and not source_record:
                plan.actions.append(Action(ActionKind.KEEP, path, "exists only in canonical target", target_sha256=target_record.sha256))
                continue

            if not target_record or not source_record:
                continue
            if target_record.sha256 == source_record.sha256:
                plan.actions.append(Action(ActionKind.KEEP, path, "identical content", source_record.sha256, target_record.sha256))
            elif target_record.file_class in {FileClass.CACHE, FileClass.GENERATED}:
                plan.actions.append(Action(ActionKind.QUARANTINE, path, f"target {target_record.file_class.value} differs", source_record.sha256, target_record.sha256))
            else:
                plan.actions.append(Action(ActionKind.CONFLICT, path, "same path has different content; target preserved", source_record.sha256, target_record.sha256))

        if target.errors:
            plan.warnings.extend(f"Target scan error: {item}" for item in target.errors)
        if source and source.errors:
            plan.warnings.extend(f"Source scan error: {item}" for item in source.errors)
        return plan
