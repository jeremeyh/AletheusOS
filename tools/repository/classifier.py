#!/usr/bin/env python3
"""
Repository artifact classifier.

The classifier is the canonical routing authority for loose repository files.
It analyzes names, suffixes, locations, and known domain conventions and
returns a proposed canonical destination without modifying the filesystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True, slots=True)
class ClassificationRule:
    """A deterministic repository classification rule."""

    name: str
    destination: Path
    prefixes: tuple[str, ...] = ()
    suffixes: tuple[str, ...] = ()
    contains: tuple[str, ...] = ()
    extensions: tuple[str, ...] = ()
    excluded_prefixes: tuple[str, ...] = ()
    priority: int = 100
    description: str = ""

    def matches(self, path: Path) -> bool:
        filename = path.name.lower()
        suffix = path.suffix.lower()

        if self.excluded_prefixes and filename.startswith(self.excluded_prefixes):
            return False

        prefix_match = not self.prefixes or filename.startswith(self.prefixes)
        suffix_match = not self.suffixes or filename.endswith(self.suffixes)
        contains_match = not self.contains or any(token in filename for token in self.contains)
        extension_match = not self.extensions or suffix in self.extensions

        return prefix_match and suffix_match and contains_match and extension_match


@dataclass(frozen=True, slots=True)
class Classification:
    """Result of classifying a repository artifact."""

    source: Path
    destination_directory: Path | None
    rule_name: str | None
    confidence: float
    reason: str
    alternatives: tuple[Path, ...] = field(default_factory=tuple)

    @property
    def classified(self) -> bool:
        return self.destination_directory is not None

    @property
    def destination(self) -> Path | None:
        if self.destination_directory is None:
            return None
        return self.destination_directory / self.source.name


class RepositoryClassifier:
    """Classifies repository artifacts using ordered deterministic rules."""

    def __init__(self, rules: Iterable[ClassificationRule]) -> None:
        self._rules = tuple(sorted(rules, key=lambda item: item.priority))

    @property
    def rules(self) -> tuple[ClassificationRule, ...]:
        return self._rules

    def classify(self, path: Path | str) -> Classification:
        source = Path(path)

        if source.name in {"__init__.py", "__main__.py"}:
            return Classification(
                source=source,
                destination_directory=None,
                rule_name=None,
                confidence=0.0,
                reason="Package control files require contextual classification.",
            )

        matches = [rule for rule in self._rules if rule.matches(source)]

        if not matches:
            return Classification(
                source=source,
                destination_directory=None,
                rule_name=None,
                confidence=0.0,
                reason="No repository classification rule matched.",
            )

        selected = matches[0]
        alternatives = tuple(
            rule.destination
            for rule in matches[1:]
            if rule.destination != selected.destination
        )

        confidence = 1.0 if len(matches) == 1 else 0.85

        return Classification(
            source=source,
            destination_directory=selected.destination,
            rule_name=selected.name,
            confidence=confidence,
            reason=selected.description or f"Matched rule {selected.name}.",
            alternatives=alternatives,
        )

    def classify_many(
        self,
        paths: Sequence[Path | str],
    ) -> list[Classification]:
        return [self.classify(path) for path in paths]


def build_default_classifier() -> RepositoryClassifier:
    """Build the canonical AletheusOS repository classifier."""

    rules = [
        ClassificationRule(
            name="genesis-post",
            destination=Path("tools/genesis/post_genesis"),
            prefixes=("post_genesis_",),
            extensions=(".sh", ".py"),
            priority=10,
            description="Post-Genesis bundle tooling belongs under post_genesis.",
        ),
        ClassificationRule(
            name="genesis-registry-federation",
            destination=Path("tools/genesis/registry_federation"),
            prefixes=("genesis_registry_federation_",),
            extensions=(".sh", ".py"),
            priority=11,
            description="Registry federation Genesis tooling.",
        ),
        ClassificationRule(
            name="genesis-card-hawk",
            destination=Path("tools/genesis/card_hawk"),
            prefixes=("genesis_card_hawk_",),
            extensions=(".sh", ".py"),
            priority=12,
            description="Card Hawk Genesis tooling.",
        ),
        ClassificationRule(
            name="genesis-universal",
            destination=Path("tools/genesis/universal"),
            prefixes=("genesis_universal_",),
            extensions=(".sh", ".py"),
            priority=13,
            description="Universal Genesis tooling.",
        ),
        ClassificationRule(
            name="genesis-script",
            destination=Path("tools/genesis"),
            prefixes=("genesis", "xogenesis"),
            extensions=(".sh", ".py"),
            priority=20,
            description="General Genesis execution tooling.",
        ),
        ClassificationRule(
            name="validation-nimble",
            destination=Path("tools/validation/nimble"),
            prefixes=("validate_nimble_",),
            extensions=(".py", ".sh"),
            priority=30,
            description="Nimble validation tooling.",
        ),
        ClassificationRule(
            name="validation-genesis",
            destination=Path("tools/validation/genesis"),
            prefixes=("validate_genesis",),
            extensions=(".py", ".sh"),
            priority=31,
            description="Genesis validation tooling.",
        ),
        ClassificationRule(
            name="validation",
            destination=Path("tools/validation"),
            prefixes=("validate_",),
            extensions=(".py", ".sh"),
            priority=40,
            description="General validation tooling.",
        ),
        ClassificationRule(
            name="verification-runtime",
            destination=Path("tools/verification/runtime"),
            prefixes=("verify_",),
            contains=(
                "runtime",
                "service",
                "event",
                "persistence",
                "reasoning",
                "state",
                "planning",
                "federation",
            ),
            extensions=(".py", ".sh"),
            priority=41,
            description="Runtime verification tooling.",
        ),
        ClassificationRule(
            name="verification-plugin",
            destination=Path("tools/verification/plugins"),
            prefixes=("verify_plugin", "verify_plugins"),
            extensions=(".py", ".sh"),
            priority=42,
            description="Plugin verification tooling.",
        ),
        ClassificationRule(
            name="verification-agent",
            destination=Path("tools/verification/agents"),
            prefixes=("verify_agent", "verify_agents"),
            extensions=(".py", ".sh"),
            priority=43,
            description="Agent verification tooling.",
        ),
        ClassificationRule(
            name="verification",
            destination=Path("tools/verification"),
            prefixes=("verify_",),
            extensions=(".py", ".sh"),
            priority=50,
            description="General verification tooling.",
        ),
        ClassificationRule(
            name="repository",
            destination=Path("tools/repository"),
            contains=("repository",),
            extensions=(".py",),
            priority=55,
            description="Repository management tooling.",
        ),
        ClassificationRule(
            name="migration",
            destination=Path("tools/migration"),
            prefixes=(
                "move_",
                "organize_",
                "migrate_",
                "migration_",
                "install_genesis",
                "step",
            ),
            extensions=(".py", ".sh"),
            priority=60,
            description="Transitional migration tooling.",
        ),
        ClassificationRule(
            name="repair",
            destination=Path("tools/repair"),
            prefixes=("repair_",),
            extensions=(".py", ".sh"),
            priority=70,
            description="Repository or runtime repair tooling.",
        ),
        ClassificationRule(
            name="remediation",
            destination=Path("tools/remediation"),
            prefixes=("remediate_",),
            extensions=(".py", ".sh"),
            priority=71,
            description="Automated remediation tooling.",
        ),
        ClassificationRule(
            name="reconciliation",
            destination=Path("tools/reconciliation"),
            prefixes=("reconcile_",),
            extensions=(".py", ".sh"),
            priority=72,
            description="State reconciliation tooling.",
        ),
        ClassificationRule(
            name="patch",
            destination=Path("tools/patch"),
            prefixes=("patch_",),
            extensions=(".py", ".sh"),
            priority=73,
            description="Targeted patch tooling.",
        ),
        ClassificationRule(
            name="planning",
            destination=Path("tools/planning"),
            prefixes=("plan_",),
            extensions=(".py", ".sh"),
            priority=74,
            description="Planning and recovery-plan tooling.",
        ),
        ClassificationRule(
            name="promotion",
            destination=Path("tools/promotion"),
            prefixes=("promote_",),
            extensions=(".py", ".sh"),
            priority=75,
            description="Promotion tooling.",
        ),
        ClassificationRule(
            name="quarantine",
            destination=Path("tools/quarantine"),
            prefixes=("quarantine_",),
            extensions=(".py", ".sh"),
            priority=76,
            description="Quarantine tooling.",
        ),
        ClassificationRule(
            name="mapping",
            destination=Path("tools/mapping"),
            prefixes=("map_",),
            extensions=(".py", ".sh"),
            priority=77,
            description="Repository mapping tooling.",
        ),
        ClassificationRule(
            name="inspection",
            destination=Path("tools/inspect"),
            prefixes=("inspect_",),
            extensions=(".py", ".sh"),
            priority=78,
            description="Inspection tooling.",
        ),
        ClassificationRule(
            name="scanning",
            destination=Path("tools/scanning"),
            prefixes=("scan_",),
            extensions=(".py", ".sh"),
            priority=79,
            description="Scanning tooling.",
        ),
        ClassificationRule(
            name="smoke",
            destination=Path("tools/smoke"),
            prefixes=("smoke_",),
            extensions=(".py", ".sh"),
            priority=80,
            description="Smoke-test tooling.",
        ),
        ClassificationRule(
            name="audit",
            destination=Path("tools/audit"),
            prefixes=("audit_",),
            extensions=(".py", ".sh"),
            priority=81,
            description="Audit tooling.",
        ),
        ClassificationRule(
            name="cleanup",
            destination=Path("tools/cleanup"),
            prefixes=("cleanup_", "remove_safe_", "archive_historical_"),
            extensions=(".py", ".sh"),
            priority=82,
            description="Cleanup and archival tooling.",
        ),
        ClassificationRule(
            name="build",
            destination=Path("tools/build"),
            prefixes=("build_",),
            extensions=(".py", ".sh"),
            priority=83,
            description="Build tooling.",
        ),
        ClassificationRule(
            name="append",
            destination=Path("tools/append"),
            prefixes=("append_",),
            extensions=(".py", ".sh"),
            priority=84,
            description="Append/update tooling.",
        ),
        ClassificationRule(
            name="collect",
            destination=Path("tools/collect"),
            prefixes=("collect_",),
            extensions=(".py", ".sh"),
            priority=85,
            description="Collection tooling.",
        ),
        ClassificationRule(
            name="compile",
            destination=Path("tools/compile"),
            prefixes=("compile_",),
            extensions=(".py", ".sh"),
            priority=86,
            description="Compilation tooling.",
        ),
        ClassificationRule(
            name="create",
            destination=Path("tools/create"),
            prefixes=("create_",),
            extensions=(".py", ".sh"),
            priority=87,
            description="Creation tooling.",
        ),
        ClassificationRule(
            name="discovery",
            destination=Path("tools/discovery"),
            prefixes=("discover_", "discovery_"),
            extensions=(".py", ".sh"),
            priority=88,
            description="Discovery tooling.",
        ),
        ClassificationRule(
            name="nimble-generate",
            destination=Path("tools/nimble"),
            prefixes=("generate_nimble_",),
            extensions=(".py", ".sh"),
            priority=90,
            description="Nimble generation tooling.",
        ),
        ClassificationRule(
            name="repository-doc",
            destination=Path("docs/repository"),
            contains=("repo", "repository"),
            extensions=(".txt", ".md", ".json", ".csv"),
            priority=100,
            description="Repository documentation or generated report.",
        ),
    ]

    return RepositoryClassifier(rules)


def classify(path: Path | str) -> Classification:
    """Convenience function using the default classifier."""

    return build_default_classifier().classify(path)


def main() -> int:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Classify repository artifacts.")
    parser.add_argument("paths", nargs="+", help="Paths to classify.")
    parser.add_argument("--json", action="store_true", help="Emit JSON.")
    args = parser.parse_args()

    classifier = build_default_classifier()
    results = classifier.classify_many([Path(item) for item in args.paths])

    if args.json:
        print(
            json.dumps(
                [
                    {
                        "source": str(item.source),
                        "classified": item.classified,
                        "destination": (
                            str(item.destination) if item.destination else None
                        ),
                        "rule": item.rule_name,
                        "confidence": item.confidence,
                        "reason": item.reason,
                        "alternatives": [str(value) for value in item.alternatives],
                    }
                    for item in results
                ],
                indent=2,
            )
        )
        return 0

    for result in results:
        if result.destination:
            print(
                f"{result.source} -> {result.destination} "
                f"[{result.rule_name}; {result.confidence:.0%}]"
            )
        else:
            print(f"{result.source} -> UNCLASSIFIED [{result.reason}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
