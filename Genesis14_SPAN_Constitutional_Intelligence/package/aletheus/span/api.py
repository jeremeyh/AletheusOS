from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from .constitutional_context import ProjectInspector
from .finding import FindingSet
from .profiles import RuleProfile, load_profile
from .reporter import SPANReport
from .rule_engine import Rule
from .rule_loader import RuleLoader
from .rule_registry import RuleRegistry


class SPAN:
    """Canonical Genesis 14 developer API for constitutional analysis."""

    def __init__(self, profile: RuleProfile | str | Path | None = None) -> None:
        if profile is None:
            self.profile = RuleProfile(name="constitutional")
        elif isinstance(profile, RuleProfile):
            self.profile = profile
        else:
            self.profile = load_profile(profile)

    def _load_rules(self) -> tuple[Rule, ...]:
        registry = RuleRegistry()
        report = RuleLoader(registry).load_all(strict=True)
        if report.errors:
            raise RuntimeError(f"SPAN rule loading failed: {report.errors}")
        return tuple(registry.values())

    def _selected_rules(self, rules: Iterable[Rule]) -> tuple[Rule, ...]:
        enabled = set(self.profile.enabled_categories)
        disabled = set(self.profile.disabled_rule_ids)
        selected = []
        for rule in rules:
            family = rule.category.split(".", 1)[0]
            if enabled and family not in enabled and rule.category not in enabled:
                continue
            if rule.id in disabled:
                continue
            selected.append(rule)
        return tuple(selected)

    def analyze(self, project_root: str | Path) -> SPANReport:
        project = ProjectInspector().inspect(project_root)
        context = project.to_rule_context()
        findings = FindingSet()

        selected = self._selected_rules(self._load_rules())
        for rule in selected:
            finding = rule.evaluate(context)
            if finding is not None:
                finding.evidence = self._evidence_for(rule.id, context)
                finding.metadata.update(
                    {
                        "profile": self.profile.name,
                        "project_root": str(project.project_root),
                    }
                )
                findings.add(finding)

        return SPANReport(
            project_root=str(project.project_root),
            profile=self.profile.name,
            findings=findings,
            metadata={
                "rules_executed": len(selected),
                "python_files": len(project.python_files),
                "genesis": "14.0",
            },
        )

    @staticmethod
    def _evidence_for(rule_id: str, context: dict) -> list:
        mapping = {
            "SPAN-CON-001": "missing_constitution",
            "SPAN-CON-002": "missing_governance_docs",
            "SPAN-ARC-001": "duplicate_namespace_candidates",
            "SPAN-ARC-002": "root_python_artifacts",
            "SPAN-RUN-001": "noncanonical_runtime_imports",
            "SPAN-RUN-002": "god_object_candidates",
            "SPAN-DEP-001": "circular_import_candidates",
            "SPAN-DEP-002": "wildcard_imports",
            "SPAN-GOV-001": "missing_span_package",
            "SPAN-GOV-002": "todo_candidates",
            "SPAN-SEC-001": "hardcoded_secret_candidates",
            "SPAN-SEC-002": "broad_exception_candidates",
            "SPAN-API-001": "mutable_default_candidates",
            "SPAN-API-002": "parse_errors",
            "SPAN-DOC-001": "missing_module_docstrings",
            "SPAN-DOC-002": "missing_public_docstrings",
            "SPAN-NAM-001": "duplicate_namespace_candidates",
            "SPAN-NAM-002": "root_python_artifacts",
            "SPAN-QUA-001": "oversized_modules",
            "SPAN-QUA-002": "print_statement_candidates",
        }
        key = mapping.get(rule_id)
        value = context.get(key) if key else None
        if isinstance(value, bool):
            return [key] if value else []
        if value is None:
            return []
        return list(value)[:25] if isinstance(value, (list, tuple, set)) else [value]
