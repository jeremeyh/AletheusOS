"""Canonical SPAN™ finding contracts and collections."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Iterator
from dataclasses import asdict, dataclass, field
from enum import Enum
from hashlib import sha256
from typing import Any


class Severity(str, Enum):
    """Canonical severity levels for SPAN findings."""

    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @classmethod
    def coerce(cls, value: Severity | str) -> Severity:
        if isinstance(value, cls):
            return value

        normalized = str(value).strip().lower()

        try:
            return cls(normalized)
        except ValueError as exc:
            allowed = ", ".join(item.value for item in cls)
            raise ValueError(
                f"unsupported severity {value!r}; expected one of: {allowed}"
            ) from exc


@dataclass(slots=True)
class Finding:
    """
    Canonical SPAN finding.

    Compatibility:
    - Existing analyzers may provide ``summary`` and omit ``id``.
    - Newer callers may provide ``description`` and an explicit ``id``.
    - Summary and description are synchronized when only one is provided.
    """

    id: str = ""
    title: str = ""
    category: str = ""
    severity: Severity = Severity.INFO

    summary: str = ""
    description: str = ""
    analyzer: str | None = None

    confidence: float = 1.0
    evidence: list[Any] = field(default_factory=list)
    recommendation: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.title = str(self.title).strip()
        self.category = str(self.category).strip()
        self.summary = str(self.summary).strip()
        self.description = str(self.description).strip()

        if self.analyzer is not None:
            normalized_analyzer = str(self.analyzer).strip()
            self.analyzer = normalized_analyzer or None

        self.severity = Severity.coerce(self.severity)

        if self.summary and not self.description:
            self.description = self.summary
        elif self.description and not self.summary:
            self.summary = self.description

        if not self.title:
            raise ValueError("finding title must not be empty")

        if not self.category:
            raise ValueError("finding category must not be empty")

        if not self.summary and not self.description:
            raise ValueError("finding must provide either summary or description")

        confidence = float(self.confidence)

        if not 0.0 <= confidence <= 1.0:
            raise ValueError("finding confidence must be between 0.0 and 1.0")

        self.confidence = confidence
        self.evidence = list(self.evidence)
        self.tags = list(
            dict.fromkeys(str(tag).strip() for tag in self.tags if str(tag).strip())
        )
        self.metadata = dict(self.metadata)

        self.id = str(self.id).strip()

        if not self.id:
            self.id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate a deterministic identifier for legacy analyzer findings."""

        identity = "\x1f".join(
            (
                self.analyzer or "unknown",
                self.category,
                self.title,
                self.summary or self.description,
            )
        )

        digest = sha256(identity.encode("utf-8")).hexdigest()[:16]

        return f"span:{self.category}:{digest}"

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["severity"] = self.severity.value
        return payload


@dataclass(slots=True)
class FindingSet:
    """Ordered collection of unique SPAN findings."""

    findings: list[Finding] = field(default_factory=list)
    _ids: set[str] = field(default_factory=set, init=False, repr=False)

    def __post_init__(self) -> None:
        initial = list(self.findings)
        self.findings = []
        self.extend(initial)

    def __iter__(self) -> Iterator[Finding]:
        return iter(self.findings)

    def __len__(self) -> int:
        return len(self.findings)

    def __bool__(self) -> bool:
        return bool(self.findings)

    def add(self, finding: Finding) -> None:
        if not isinstance(finding, Finding):
            raise TypeError(
                f"FindingSet accepts Finding instances, got {type(finding).__name__}"
            )

        if finding.id in self._ids:
            raise ValueError(f"duplicate finding id: {finding.id}")

        self.findings.append(finding)
        self._ids.add(finding.id)

    def extend(self, findings: Iterable[Finding]) -> None:
        for finding in findings:
            self.add(finding)

    def get(self, finding_id: str) -> Finding:
        for finding in self.findings:
            if finding.id == finding_id:
                return finding

        raise KeyError(finding_id)

    def by_severity(
        self,
        severity: Severity | str,
    ) -> tuple[Finding, ...]:
        expected = Severity.coerce(severity)

        return tuple(
            finding for finding in self.findings if finding.severity is expected
        )

    def by_category(self, category: str) -> tuple[Finding, ...]:
        return tuple(
            finding for finding in self.findings if finding.category == category
        )

    def summary(self) -> dict[str, Any]:
        severity_counts = Counter(finding.severity.value for finding in self.findings)
        category_counts = Counter(finding.category for finding in self.findings)

        return {
            "total": len(self.findings),
            "by_severity": {
                severity.value: severity_counts.get(severity.value, 0)
                for severity in Severity
            },
            "by_category": dict(sorted(category_counts.items())),
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary": self.summary(),
            "findings": [finding.to_dict() for finding in self.findings],
        }
