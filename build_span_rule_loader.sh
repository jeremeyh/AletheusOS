#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="${1:-$(pwd)}"
cd "$ROOT"

TARGET="aletheus/span/rule_loader.py"
RULES_DIR="aletheus/span/rules"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
BACKUP_DIR="reports/span/backups/rule_loader_${STAMP}"

if [[ ! -d "aletheus/span" ]]; then
    echo "ERROR: aletheus/span directory not found."
    echo "Run this builder from the AletheusOS project root."
    exit 1
fi

if [[ ! -f "aletheus/span/rule_engine.py" ]]; then
    echo "ERROR: aletheus/span/rule_engine.py not found."
    exit 1
fi

if [[ ! -f "aletheus/span/rule_registry.py" ]]; then
    echo "ERROR: aletheus/span/rule_registry.py not found."
    exit 1
fi

mkdir -p "$BACKUP_DIR" "$RULES_DIR"

if [[ -f "$TARGET" ]]; then
    cp "$TARGET" "$BACKUP_DIR/rule_loader.py"
fi

if [[ -f "$RULES_DIR/__init__.py" ]]; then
    cp "$RULES_DIR/__init__.py" "$BACKUP_DIR/rules___init__.py"
fi

cat > "$RULES_DIR/__init__.py" <<'PY'
"""Built-in SPAN™ rule modules.

Rule modules may export:

- Individual ``Rule`` instances.
- A ``RULES`` iterable containing ``Rule`` instances.

The RuleLoader discovers modules in this package automatically.
"""
PY

cat > "$TARGET" <<'PY'
"""Automatic discovery and registration for SPAN™ rules."""

from __future__ import annotations

import importlib
import inspect
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
PY

echo
echo "Compiling Rule Loader..."

python -m py_compile \
    aletheus/span/rule_loader.py \
    aletheus/span/rule_registry.py \
    aletheus/span/rule_engine.py \
    aletheus/span/rules/__init__.py

echo
echo "Running Genesis 13.4 validation..."

python - <<'PY'
from types import ModuleType

from aletheus.span.finding import Severity
from aletheus.span.rule_engine import Rule
from aletheus.span.rule_loader import RuleLoader, RuleLoadReport
from aletheus.span.rule_registry import RuleRegistry


def make_rule(rule_id: str) -> Rule:
    return Rule(
        id=rule_id,
        title=f"Validation rule {rule_id}",
        category="loader",
        severity=Severity.INFO,
        predicate=lambda context: True,
    )


registry = RuleRegistry()
loader = RuleLoader(registry)

single = make_rule("SPAN-LOADER-001")
grouped = make_rule("SPAN-LOADER-002")

module = ModuleType("aletheus.span.rules.validation_fixture")
module.SINGLE_RULE = single
module.RULES = (single, grouped)

extracted = loader.extract_rules(module)

assert extracted == (single, grouped)
assert loader.validate(single) == ()

report = RuleLoadReport(package=loader.package)
loader.register_module(module, report)

assert report.ok
assert report.registered_rule_ids == [
    "SPAN-LOADER-001",
    "SPAN-LOADER-002",
]
assert len(registry) == 2

duplicate_report = RuleLoadReport(package=loader.package)
loader.register_module(module, duplicate_report)

assert duplicate_report.error_count == 0
assert duplicate_report.warning_count == 2
assert len(registry) == 2

engine = registry.build_engine()
findings = engine.evaluate({})

assert findings.summary()["total"] == 2

discovery_report = loader.load_all(strict=True)

assert discovery_report.ok
assert discovery_report.package == "aletheus.span.rules"

print("RuleLoader import: OK")
print("Individual export extraction: OK")
print("RULES collection extraction: OK")
print("Duplicate object normalization: OK")
print("Rule validation: OK")
print("Registry registration: OK")
print("Duplicate registry protection: OK")
print("Package discovery: OK")
print("RuleEngine composition: OK")
print("Validation findings:", findings.summary())
print("Discovery:", discovery_report.summary())
PY

echo
echo "Verifying public contracts..."

grep -nE \
    'class RuleLoader|class RuleLoadReport|def discover|def extract_rules|def load_all' \
    "$TARGET"

echo
echo "========================================="
echo "Genesis 13.4 Rule Loader"
echo "Installed and validated successfully."
echo "========================================="
echo
echo "Created:"
echo "  $TARGET"
echo "  $RULES_DIR/__init__.py"
echo
echo "Backup:"
echo "  $BACKUP_DIR"
