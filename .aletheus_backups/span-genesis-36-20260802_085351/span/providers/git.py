"""Git repository evidence provider for SPAN™."""

from __future__ import annotations

import subprocess
from pathlib import Path

from ..evidence_store import EvidenceRecord
from .base import Provider, ProviderContext


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


class GitProvider(Provider):
    name = "git"
    version = "1.0.0"
    description = "Collect repository state, branch, head, and recent change evidence."

    def __init__(self, *, history_limit: int = 250) -> None:
        self.history_limit = max(1, history_limit)

    def collect(self, context: ProviderContext):
        root = context.root.resolve()
        inside = _run_git(root, "rev-parse", "--is-inside-work-tree")
        if inside.returncode != 0 or inside.stdout.strip() != "true":
            yield EvidenceRecord(
                kind="git_unavailable",
                provider=self.name,
                source=".",
                location=str(root),
                payload={"message": inside.stderr.strip() or "Not a Git work tree."},
                tags=("git", "warning"),
            )
            return

        branch = _run_git(root, "branch", "--show-current").stdout.strip()
        head = _run_git(root, "rev-parse", "HEAD").stdout.strip()
        status = _run_git(root, "status", "--porcelain=v1").stdout.splitlines()

        yield EvidenceRecord(
            kind="git_repository",
            provider=self.name,
            source=".",
            location=str(root),
            payload={
                "branch": branch,
                "head": head,
                "dirty": bool(status),
                "changed_paths": len(status),
            },
            tags=("git", "repository"),
        )

        for line in status:
            if len(line) < 4:
                continue
            status_code = line[:2]
            path = line[3:]
            yield EvidenceRecord(
                kind="git_change",
                provider=self.name,
                source=path,
                location=str(root / path),
                payload={"path": path, "status": status_code},
                tags=("git", "change"),
            )

        log_result = _run_git(
            root,
            "log",
            f"-n{self.history_limit}",
            "--name-only",
            "--pretty=format:__SPAN_COMMIT__%H|%aI|%ae",
        )
        if log_result.returncode != 0:
            return

        current_commit: dict[str, str] | None = None
        for raw in log_result.stdout.splitlines():
            line = raw.strip()
            if not line:
                continue
            if line.startswith("__SPAN_COMMIT__"):
                commit_hash, authored_at, author_email = line.removeprefix(
                    "__SPAN_COMMIT__"
                ).split("|", 2)
                current_commit = {
                    "commit": commit_hash,
                    "authored_at": authored_at,
                    "author_email": author_email,
                }
                continue
            if current_commit is None:
                continue
            yield EvidenceRecord(
                kind="git_file_history",
                provider=self.name,
                source=line,
                location=str(root / line),
                payload={**current_commit, "path": line},
                tags=("git", "history"),
            )
