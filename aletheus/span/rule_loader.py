"""Automatic discovery and registration for SPAN™ rules."""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, field
from types import ModuleType
from typing import Any

from .rule_engine import Rule
from .rule_registry import RuleRegistry


@dataclass(frozen=True, slots=True)
class RuleLoadDiagnostic:
    """One informational, warning, or error event from rule loading."""

    level: str
    code: str
    message: str
    module: str | None = None
    rule_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "level": self.level,
            "code": self.code,
            "message": self.message,
            "module": self.module,
            "rule_id": self.rule_id,
        }


@dataclass(slots=True)
class RuleLoadReport:
    """Summary of one RuleLoader execution."""

    package: str
    discovered_modules: list[str] = field(default_factory=list)
    imported_modules: list[str] = field(default_factory=list)
    registered_rule_ids: list[str] = field(default_factory=list)
    diagnostics: list[RuleLoadDiagnostic] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(item.level == "error" for item in self.diagnostics)

    @property
    def warning_count(self) -> int:
        return sum(item.level == "warning" for item in self.diagnostics)

    @property
    def ok(self) -> bool:
        return self.error_count == 0

    def add(
        self,
        level: str,
        code: str,
        message: str,
        *,
        module: str | None = None,
        rule_id: str | None = None,
    ) -> None:
        self.diagnostics.append(
            RuleLoadDiagnostic(
                level=level,
                code=code,
                message=message,
                module=module,
                rule_id=rule_id,
            )
        )

    def summary(self) -> dict[str, Any]:
        return {
            "package": self.package,
            "ok": self.ok,
            "modules_discovered": len(self.discovered_modules),
            "modules_imported": len(self.imported_modules),
            "rules_registered": len(self.registered_rule_ids),
            "warnings": self.warning_count,
            "errors": self.error_count,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "discovered_modules": list(self.discovered_modules),
            "imported_modules": list(self.imported_modules),
            "registered_rule_ids": list(self.registered_rule_ids),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }


class RuleLoader:
    """Discover, validate, and register SPAN rules from a Python package."""

    def __init__(
        self,
        registry: RuleRegistry,
        package: str = "aletheus.span.rules",
    ) -> None:
        if not isinstance(registry, RuleRegistry):
            raise TypeError(
                "registry must be a RuleRegistry, "
                f"got {type(registry).__name__}"
            )

        package = str(package).strip()
        if not package:
            raise ValueError("package must not be empty")

        self.registry = registry
        self.package = package

    def discover(self) -> tuple[str, ...]:
        """Return import paths for all modules in the configured package."""

        package_module = importlib.import_module(self.package)
        package_path = getattr(package_module, "__path__", None)

        if package_path is None:
            raise ValueError(
                f"configured rule package is not a package: {self.package}"
            )

        modules = {
            module_info.name
            for module_info in pkgutil.walk_packages(
                package_path,
                prefix=f"{self.package}.",
            )
            if not module_info.ispkg
            and not module_info.name.rsplit(".", 1)[-1].startswith("_")
        }

        return tuple(sorted(modules))

    @staticmethod
    def import_module(module_name: str) -> ModuleType:
        """Import and return one rule module."""

        return importlib.import_module(module_name)

    @classmethod
    def extract_rules(cls, module: ModuleType) -> tuple[Rule, ...]:
        """
        Extract public Rule exports from a module.

        Supported forms:

        - ``MY_RULE = Rule(...)``
        - ``RULES = (Rule(...), Rule(...))``
        - Public mappings or iterables that contain Rule objects

        Duplicate object references and duplicate IDs within a module are
        collapsed during extraction.
        """

        candidates: list[Rule] = []

        for name, value in vars(module).items():
            if name.startswith("_"):
                continue

            if isinstance(value, Rule):
                candidates.append(value)
                continue

            if name == "RULES":
                candidates.extend(cls._rules_from_container(value))

        unique: list[Rule] = []
        seen_objects: set[int] = set()
        seen_ids: set[str] = set()

        for rule in candidates:
            object_identity = id(rule)
            rule_id = str(getattr(rule, "id", "")).strip()

            if object_identity in seen_objects:
                continue

            if rule_id and rule_id in seen_ids:
                continue

            seen_objects.add(object_identity)
            if rule_id:
                seen_ids.add(rule_id)

            unique.append(rule)

        return tuple(unique)

    @staticmethod
    def _rules_from_container(value: Any) -> list[Rule]:
        if isinstance(value, Mapping):
            iterable: Iterable[Any] = value.values()
        elif isinstance(value, Iterable) and not isinstance(
            value,
            (str, bytes, bytearray),
        ):
            iterable = value
        else:
            raise TypeError(
                "RULES must be an iterable or mapping of Rule instances"
            )

        rules: list[Rule] = []

        for item in iterable:
            if not isinstance(item, Rule):
                raise TypeError(
                    "RULES contains a non-Rule value: "
                    f"{type(item).__name__}"
                )
            rules.append(item)

        return rules

    @staticmethod
    def validate(rule: Rule) -> tuple[str, ...]:
        """Return validation errors for one rule."""

        errors: list[str] = []

        if not isinstance(rule, Rule):
            return (f"expected Rule, got {type(rule).__name__}",)

        rule_id = str(getattr(rule, "id", "")).strip()
        title = str(getattr(rule, "title", "")).strip()
        category = str(getattr(rule, "category", "")).strip()
        predicate = getattr(rule, "predicate", None)

        if not rule_id:
            errors.append("rule id must not be empty")

        if not title:
            errors.append("rule title must not be empty")

        if not category:
            errors.append("rule category must not be empty")

        if not callable(predicate):
            errors.append("rule predicate must be callable")

        return tuple(errors)

    def register_module(
        self,
        module: ModuleType,
        report: RuleLoadReport,
    ) -> None:
        """Extract and register valid rules from one imported module."""

        try:
            rules = self.extract_rules(module)
        except Exception as exc:
            report.add(
                "error",
                "rule_extraction_failed",
                f"{type(exc).__name__}: {exc}",
                module=module.__name__,
            )
            return

        if not rules:
            report.add(
                "warning",
                "no_rules_found",
                "Module exported no discoverable Rule instances.",
                module=module.__name__,
            )
            return

        for rule in rules:
            rule_id = str(getattr(rule, "id", "")).strip() or None
            validation_errors = self.validate(rule)

            if validation_errors:
                report.add(
                    "error",
                    "invalid_rule",
                    "; ".join(validation_errors),
                    module=module.__name__,
                    rule_id=rule_id,
                )
                continue

            assert rule_id is not None

            if rule_id in self.registry:
                report.add(
                    "warning",
                    "duplicate_rule",
                    "Rule ID is already registered; skipped.",
                    module=module.__name__,
                    rule_id=rule_id,
                )
                continue

            try:
                self.registry.register(rule)
            except Exception as exc:
                report.add(
                    "error",
                    "registration_failed",
                    f"{type(exc).__name__}: {exc}",
                    module=module.__name__,
                    rule_id=rule_id,
                )
                continue

            report.registered_rule_ids.append(rule_id)
            report.add(
                "info",
                "rule_registered",
                "Rule registered successfully.",
                module=module.__name__,
                rule_id=rule_id,
            )

    def load_all(self, *, strict: bool = False) -> RuleLoadReport:
        """
        Discover, import, validate, and register every rule module.

        When ``strict`` is true, a RuntimeError is raised after loading if any
        errors were collected. The report remains available on the exception
        through ``exception.report``.
        """

        report = RuleLoadReport(package=self.package)

        try:
            report.discovered_modules.extend(self.discover())
        except Exception as exc:
            report.add(
                "error",
                "discovery_failed",
                f"{type(exc).__name__}: {exc}",
                module=self.package,
            )
            self._raise_if_strict(report, strict)
            return report

        for module_name in report.discovered_modules:
            try:
                module = self.import_module(module_name)
            except Exception as exc:
                report.add(
                    "error",
                    "module_import_failed",
                    f"{type(exc).__name__}: {exc}",
                    module=module_name,
                )
                continue

            report.imported_modules.append(module_name)
            self.register_module(module, report)

        self._raise_if_strict(report, strict)
        return report

    @staticmethod
    def _raise_if_strict(
        report: RuleLoadReport,
        strict: bool,
    ) -> None:
        if not strict or report.ok:
            return

        error = RuntimeError(
            "Rule loading failed with "
            f"{report.error_count} error(s)."
        )
        error.report = report  # type: ignore[attr-defined]
        raise error
