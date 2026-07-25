#!/usr/bin/env python3
"""Repository structural policy rules."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .classifier import RepositoryClassifier, build_default_classifier
from .inventory import InventoryEntry


@dataclass(frozen=True, slots=True)
class PolicyViolation:
    code: str
    severity: str
    path: Path
    message: str
    recommendation: str


class RepositoryPolicy:
    DEFAULT_ALLOWED_ROOT_FILES = {
        ".editorconfig",
        ".gitignore",
        ".pre-commit-config.yaml",
        "ARCHITECTURE.md",
        "CHANGELOG.md",
        "Dockerfile",
        "Dockerfile.nimble",
        "FEATURES.md",
        "LICENSE",
        "Makefile",
        "MAPPING.md",
        "MIGRATION.md",
        "README.md",
        "ROADMAP.md",
        "SECURITY.md",
        "VERSION",
        "app.py",
        "compose.nimble.yml",
        "manage.py",
        "pyproject.toml",
        "release_manifest.json",
        "requirements.txt",
        "requirements_aletheus.txt",
        "run.py",
        "run_aletheus_founder_console.py",
        "run_aletheus_system_test.sh",
        "run_repository_self_repair.sh",
    }

    def __init__(
        self,
        allowed_root_files: Iterable[str] | None = None,
        classifier: RepositoryClassifier | None = None,
    ) -> None:
        self.allowed_root_files = set(
            allowed_root_files or self.DEFAULT_ALLOWED_ROOT_FILES
        )
        self.classifier = classifier or build_default_classifier()

    def evaluate(self, entries: Iterable[InventoryEntry]) -> list[PolicyViolation]:
        violations: list[PolicyViolation] = []

        for entry in entries:
            relative = entry.relative_path

            if len(relative.parts) != 1:
                continue

            if relative.name in self.allowed_root_files:
                continue

            classification = self.classifier.classify(relative)

            if classification.destination:
                violations.append(
                    PolicyViolation(
                        code="ROOT_TOOLING",
                        severity="warning",
                        path=relative,
                        message="Classifiable artifact remains in repository root.",
                        recommendation=f"Move to {classification.destination}.",
                    )
                )
            elif relative.suffix in {".py", ".sh"}:
                violations.append(
                    PolicyViolation(
                        code="ROOT_EXECUTABLE",
                        severity="error",
                        path=relative,
                        message="Unapproved executable remains in repository root.",
                        recommendation="Classify manually and move into tools/.",
                    )
                )
            else:
                violations.append(
                    PolicyViolation(
                        code="ROOT_UNCLASSIFIED",
                        severity="warning",
                        path=relative,
                        message="Unapproved artifact remains in repository root.",
                        recommendation="Move into docs/, config/, reports/, or tools/.",
                    )
                )

        return violations
