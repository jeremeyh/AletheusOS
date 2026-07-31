#!/usr/bin/env python3
"""AletheusOS policy-driven repository health auditor."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_POLICY = REPOSITORY_ROOT / "config" / "repository_policy.json"
REPORT_DIRECTORY = REPOSITORY_ROOT / "reports" / "repository"
SNAPSHOT_DIRECTORY = REPORT_DIRECTORY / "snapshots"


@dataclass(frozen=True)
class Finding:
    severity: str
    category: str
    path: str
    message: str
    recommendation: str = ""


@dataclass
class HealthResult:
    score: float
    dimensions: dict[str, float]
    counts: dict[str, int]
    files: int
    directories: int
    findings: list[Finding]
    drift: dict[str, Any]


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def load_policy(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise SystemExit(f"Repository policy not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid repository policy JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("Repository policy must contain a JSON object.")

    return data


def normalized_set(policy: dict[str, Any], key: str) -> set[str]:
    value = policy.get(key, [])
    return {str(item) for item in value if isinstance(item, str)}


def is_executable(path: Path) -> bool:
    try:
        mode = path.stat().st_mode
    except OSError:
        return False

    if bool(mode & stat.S_IXUSR):
        return True

    return path.suffix.lower() in {".py", ".sh", ".bash", ".zsh"}


def contains_control_characters(name: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in name)


def iter_repository_entries(
    root: Path,
    ignored_directories: set[str],
) -> Iterable[Path]:
    for current_root, directories, files in os.walk(root):
        current = Path(current_root)

        directories[:] = [
            directory
            for directory in directories
            if directory not in ignored_directories
        ]

        for directory in directories:
            yield current / directory

        for filename in files:
            yield current / filename


def hash_manifest(entries: Iterable[Path], root: Path) -> str:
    digest = hashlib.sha256()

    for entry in sorted(entries, key=lambda item: str(item.relative_to(root))):
        relative = str(entry.relative_to(root))
        digest.update(relative.encode("utf-8", errors="surrogateescape"))

        try:
            metadata = entry.stat()
        except OSError:
            continue

        digest.update(str(metadata.st_size).encode("ascii"))
        digest.update(str(metadata.st_mtime_ns).encode("ascii"))

    return digest.hexdigest()


def root_findings(root: Path, policy: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []

    allowed = (
        normalized_set(policy, "allowed_root_documents")
        | normalized_set(policy, "allowed_root_configuration")
        | normalized_set(policy, "allowed_root_entrypoints")
    )
    ignored_files = normalized_set(policy, "ignored_files")
    protected = normalized_set(policy, "protected_root_files")
    approved_protected = normalized_set(
        policy,
        "approved_protected_root_files",
    )
    classifications = policy.get("root_file_classifications", {})
    deterministic = policy.get("deterministic_moves", {})

    for entry in sorted(root.iterdir(), key=lambda item: item.name.casefold()):
        if entry.is_dir():
            continue

        name = entry.name

        if contains_control_characters(name):
            findings.append(
                Finding(
                    severity="error",
                    category="naming",
                    path=name,
                    message="Filename contains newline or control characters.",
                    recommendation="Rename the artifact to a stable, portable filename.",
                )
            )
            continue

        if name in ignored_files:
            findings.append(
                Finding(
                    severity="warning",
                    category="hygiene",
                    path=name,
                    message="Ignored operating-system or generated artifact exists.",
                    recommendation="Remove the artifact and keep it ignored by Git.",
                )
            )
            continue

        if name in allowed:
            continue

        if name in deterministic:
            findings.append(
                Finding(
                    severity="warning",
                    category="organization",
                    path=name,
                    message="Deterministically classifiable artifact remains in root.",
                    recommendation=f"Move to {deterministic[name]}.",
                )
            )
            continue

        if name in protected:
            if name in approved_protected:
                continue
            classification = classifications.get(name, "protected-root-review")
            findings.append(
                Finding(
                    severity="policy",
                    category="classification",
                    path=name,
                    message=f"Protected artifact requires an explicit architecture decision: {classification}.",
                    recommendation="Keep in place until imports and entry-point ownership are verified.",
                )
            )
            continue

        if is_executable(entry):
            findings.append(
                Finding(
                    severity="error",
                    category="organization",
                    path=name,
                    message="Unapproved executable remains in repository root.",
                    recommendation="Classify it as an entry point, migration, utility, or application component.",
                )
            )
        else:
            findings.append(
                Finding(
                    severity="warning",
                    category="organization",
                    path=name,
                    message="Unapproved artifact remains in repository root.",
                    recommendation="Classify, archive, document, or remove it.",
                )
            )

    return findings


def namespace_findings(
    root: Path,
    policy: dict[str, Any],
) -> list[Finding]:
    findings: list[Finding] = []

    duplicate_pairs = [
        ("event_bus", "eventbus"),
        ("backup", "backups"),
        ("card_hawk", "cardhawk"),
        ("workflow", "workflows"),
        ("engine", "engines"),
    ]

    approved_pairs = {
        tuple(pair) for pair in policy.get("approved_namespace_pairs", [])
    }

    for left, right in duplicate_pairs:
        if (left, right) in approved_pairs:
            continue
        if (root / left).exists() and (root / right).exists():
            findings.append(
                Finding(
                    severity="policy",
                    category="boundary",
                    path=f"{left} ↔ {right}",
                    message="Parallel namespaces may represent duplicate ownership or historical lineage.",
                    recommendation="Create an ADR identifying the canonical namespace and compatibility boundary.",
                )
            )

    high_risk_roots = {
        "core",
        "runtime",
        "kernel",
        "engine",
        "engines",
        "architecture",
        "repository",
    }

    for name in sorted(high_risk_roots):
        path = root / name
        if path.is_dir():
            findings.append(
                Finding(
                    severity="info",
                    category="boundary",
                    path=name,
                    message="High-authority root namespace exists outside the canonical aletheus package.",
                    recommendation="Verify whether it is canonical, compatibility, application-specific, or legacy.",
                )
            )

    return findings


def empty_directory_findings(
    root: Path,
    ignored_directories: set[str],
) -> list[Finding]:
    findings: list[Finding] = []

    for current_root, directories, files in os.walk(root, topdown=False):
        current = Path(current_root)

        if current == root:
            continue

        if any(part in ignored_directories for part in current.relative_to(root).parts):
            continue

        try:
            is_empty = not any(current.iterdir())
        except OSError:
            continue

        if is_empty:
            findings.append(
                Finding(
                    severity="info",
                    category="hygiene",
                    path=str(current.relative_to(root)),
                    message="Empty directory detected.",
                    recommendation="Remove it if it is not an intentional namespace placeholder.",
                )
            )

    return findings


def calculate_dimensions(findings: list[Finding]) -> dict[str, float]:
    categories = {
        "organization": 100.0,
        "policy": 100.0,
        "naming": 100.0,
        "drift": 100.0,
        "hygiene": 100.0,
    }

    penalties = {
        "critical": 20.0,
        "error": 5.0,
        "warning": 1.0,
        "policy": 0.5,
        "info": 0.0,
    }

    category_map = {
        "organization": "organization",
        "classification": "policy",
        "boundary": "policy",
        "naming": "naming",
        "hygiene": "hygiene",
        "drift": "drift",
    }

    for finding in findings:
        dimension = category_map.get(finding.category, "policy")
        categories[dimension] -= penalties.get(finding.severity, 1.0)

    return {
        key: round(max(0.0, min(100.0, value)), 2) for key, value in categories.items()
    }


def weighted_score(
    dimensions: dict[str, float],
    policy: dict[str, Any],
) -> float:
    configured = policy.get("health_dimensions", {})
    defaults = {
        "organization": 0.30,
        "policy": 0.25,
        "naming": 0.15,
        "drift": 0.15,
        "hygiene": 0.15,
    }

    weights = {
        key: float(configured.get(key, default)) for key, default in defaults.items()
    }

    total_weight = sum(weights.values()) or 1.0
    result = sum(dimensions[key] * weights[key] for key in defaults)
    return round(max(0.0, min(100.0, result / total_weight)), 2)


def load_latest_snapshot() -> dict[str, Any] | None:
    if not SNAPSHOT_DIRECTORY.exists():
        return None

    snapshots = sorted(SNAPSHOT_DIRECTORY.glob("repository-*.json"))

    if not snapshots:
        return None

    try:
        return json.loads(snapshots[-1].read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def build_snapshot(
    root: Path,
    entries: list[Path],
    file_count: int,
    directory_count: int,
) -> dict[str, Any]:
    root_names = sorted(item.name for item in root.iterdir())

    return {
        "generated_at": utc_now(),
        "repository": root.name,
        "files": file_count,
        "directories": directory_count,
        "root_entries": root_names,
        "manifest_sha256": hash_manifest(entries, root),
    }


def compare_snapshots(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> dict[str, Any]:
    if previous is None:
        return {
            "baseline": True,
            "files_added": 0,
            "files_removed": 0,
            "directories_added": 0,
            "directories_removed": 0,
            "root_entries_added": [],
            "root_entries_removed": [],
            "manifest_changed": False,
        }

    previous_root = set(previous.get("root_entries", []))
    current_root = set(current.get("root_entries", []))

    return {
        "baseline": False,
        "files_added": max(0, current["files"] - int(previous.get("files", 0))),
        "files_removed": max(0, int(previous.get("files", 0)) - current["files"]),
        "directories_added": max(
            0,
            current["directories"] - int(previous.get("directories", 0)),
        ),
        "directories_removed": max(
            0,
            int(previous.get("directories", 0)) - current["directories"],
        ),
        "root_entries_added": sorted(current_root - previous_root),
        "root_entries_removed": sorted(previous_root - current_root),
        "manifest_changed": (
            current.get("manifest_sha256") != previous.get("manifest_sha256")
        ),
    }


def write_snapshot(snapshot: dict[str, Any]) -> Path:
    SNAPSHOT_DIRECTORY.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = SNAPSHOT_DIRECTORY / f"repository-{stamp}.json"
    path.write_text(
        json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return path


def write_reports(
    result: HealthResult, snapshot_path: Path | None
) -> tuple[Path, Path]:
    REPORT_DIRECTORY.mkdir(parents=True, exist_ok=True)

    json_path = REPORT_DIRECTORY / "repository-health.json"
    markdown_path = REPORT_DIRECTORY / "repository-health.md"

    payload = {
        "generated_at": utc_now(),
        "health_score": result.score,
        "dimensions": result.dimensions,
        "counts": result.counts,
        "files": result.files,
        "directories": result.directories,
        "drift": result.drift,
        "snapshot": str(snapshot_path.relative_to(REPOSITORY_ROOT))
        if snapshot_path
        else None,
        "findings": [asdict(item) for item in result.findings],
    }

    json_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# AletheusOS Repository Health",
        "",
        f"Generated: `{payload['generated_at']}`",
        "",
        "## Summary",
        "",
        f"- Overall health: **{result.score:.2f}%**",
        f"- Files: **{result.files}**",
        f"- Directories: **{result.directories}**",
        f"- Errors: **{result.counts.get('error', 0)}**",
        f"- Warnings: **{result.counts.get('warning', 0)}**",
        f"- Policy findings: **{result.counts.get('policy', 0)}**",
        "",
        "## Health Dimensions",
        "",
        "| Dimension | Score |",
        "|---|---:|",
    ]

    for name, score in result.dimensions.items():
        lines.append(f"| {name.title()} | {score:.2f}% |")

    lines.extend(
        [
            "",
            "## Repository Drift",
            "",
            f"- Baseline snapshot: **{result.drift.get('baseline', False)}**",
            f"- Files added: **{result.drift.get('files_added', 0)}**",
            f"- Files removed: **{result.drift.get('files_removed', 0)}**",
            f"- Directories added: **{result.drift.get('directories_added', 0)}**",
            f"- Directories removed: **{result.drift.get('directories_removed', 0)}**",
            "",
            "## Findings",
            "",
        ]
    )

    if not result.findings:
        lines.append("No repository findings were detected.")
    else:
        for finding in result.findings:
            lines.extend(
                [
                    f"### {finding.severity.upper()} — `{finding.path}`",
                    "",
                    f"- Category: `{finding.category}`",
                    f"- Finding: {finding.message}",
                ]
            )
            if finding.recommendation:
                lines.append(f"- Recommendation: {finding.recommendation}")
            lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return markdown_path, json_path


def run_doctor(
    policy_path: Path,
    save_snapshot: bool = True,
) -> HealthResult:
    policy = load_policy(policy_path)
    ignored_directories = normalized_set(policy, "ignored_directories")

    entries = list(iter_repository_entries(REPOSITORY_ROOT, ignored_directories))
    files = sum(1 for item in entries if item.is_file())
    directories = sum(1 for item in entries if item.is_dir())

    findings = root_findings(REPOSITORY_ROOT, policy)
    findings.extend(namespace_findings(REPOSITORY_ROOT, policy))
    findings.extend(empty_directory_findings(REPOSITORY_ROOT, ignored_directories))

    snapshot = build_snapshot(REPOSITORY_ROOT, entries, files, directories)
    previous = load_latest_snapshot()
    drift = compare_snapshots(previous, snapshot)

    if drift.get("root_entries_added"):
        findings.append(
            Finding(
                severity="info",
                category="drift",
                path="repository-root",
                message=(
                    "New root entries detected: "
                    + ", ".join(drift["root_entries_added"])
                ),
                recommendation="Review whether each new root entry is constitutionally permitted.",
            )
        )

    dimensions = calculate_dimensions(findings)
    score = weighted_score(dimensions, policy)

    counts: dict[str, int] = {
        "critical": 0,
        "error": 0,
        "warning": 0,
        "policy": 0,
        "info": 0,
    }

    for finding in findings:
        counts[finding.severity] = counts.get(finding.severity, 0) + 1

    result = HealthResult(
        score=score,
        dimensions=dimensions,
        counts=counts,
        files=files,
        directories=directories,
        findings=findings,
        drift=drift,
    )

    snapshot_path = write_snapshot(snapshot) if save_snapshot else None
    markdown_path, json_path = write_reports(result, snapshot_path)

    print("AletheusOS Repository Doctor")
    print("=" * 48)
    print(f"Health score: {result.score:.2f}%")
    print(f"Files:        {result.files}")
    print(f"Directories:  {result.directories}")
    print(f"Errors:       {result.counts.get('error', 0)}")
    print(f"Warnings:     {result.counts.get('warning', 0)}")
    print(f"Policy:       {result.counts.get('policy', 0)}")
    print(f"Markdown:     {markdown_path.relative_to(REPOSITORY_ROOT)}")
    print(f"JSON:         {json_path.relative_to(REPOSITORY_ROOT)}")

    for finding in result.findings:
        if finding.severity == "info":
            continue
        print(f"[{finding.severity.upper()}] {finding.path}: {finding.message}")

    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit AletheusOS repository health and policy compliance."
    )
    parser.add_argument(
        "--policy",
        type=Path,
        default=DEFAULT_POLICY,
        help="Path to repository policy JSON.",
    )
    parser.add_argument(
        "--no-snapshot",
        action="store_true",
        help="Do not save a repository drift snapshot.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit nonzero when error or critical findings exist.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = run_doctor(
        policy_path=args.policy,
        save_snapshot=not args.no_snapshot,
    )

    if args.strict and (
        result.counts.get("critical", 0) > 0 or result.counts.get("error", 0) > 0
    ):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
