#!/usr/bin/env bash
set -euo pipefail

# 𝒙𝑜Genesis™ Engineering Drop 012A
# SPAN™ Foundation
# Spectrum Platform Analyzer & Navigator™
#
# SPARTAN™
# Spatial Platform Analysis Recursive Transformative Autogenous Network™
#
# Run from the repository root:
#   bash xogenesis_drop_012A_span_foundation.sh
#
# Optional:
#   ALETHEUS_PACKAGE_ROOT=src/aletheus bash xogenesis_drop_012A_span_foundation.sh
#
# Default package root:
#   aletheus

ROOT="${ALETHEUS_PACKAGE_ROOT:-aletheus}"
STRATEGIC="${ROOT}/strategic"
SPAN="${STRATEGIC}/span"
SPARTAN="${STRATEGIC}/spartan"
TESTS="${ALETHEUS_TEST_ROOT:-tests/strategic}"

echo "Installing 𝒙𝑜Genesis™ Engineering Drop 012A..."
echo "Package root: ${ROOT}"

mkdir -p \
  "${SPAN}" \
  "${SPARTAN}" \
  "${TESTS}"

cat > "${STRATEGIC}/__init__.py" <<'PY'
"""Strategic Intelligence Domain for AletheusOS™.

Canonical capabilities:
- SPAN™: Spectrum Platform Analyzer & Navigator™
- SPARTAN™: Spatial Platform Analysis Recursive Transformative Autogenous Network™
"""

from .span import SPANCapability, build_span
from .spartan import SPARTANNetwork, build_spartan

__all__ = [
    "SPANCapability",
    "SPARTANNetwork",
    "build_span",
    "build_spartan",
]
PY

cat > "${SPAN}/__init__.py" <<'PY'
"""SPAN™ — Spectrum Platform Analyzer & Navigator™."""

from .capability import SPANCapability
from .config import SPANConfig
from .factory import build_span
from .models import (
    AnalysisRequest,
    AnalysisResult,
    ConstitutionalAssessment,
    Evidence,
    NavigationPlan,
    Recommendation,
    RecommendationPriority,
    RecommendationStatus,
    RiskLevel,
)

__all__ = [
    "SPANCapability",
    "SPANConfig",
    "AnalysisRequest",
    "AnalysisResult",
    "ConstitutionalAssessment",
    "Evidence",
    "NavigationPlan",
    "Recommendation",
    "RecommendationPriority",
    "RecommendationStatus",
    "RiskLevel",
    "build_span",
]
PY

cat > "${SPAN}/config.py" <<'PY'
"""Configuration for SPAN™."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta


@dataclass(frozen=True, slots=True)
class SPANConfig:
    """Runtime configuration for SPAN™.

    The defaults intentionally favor advisory behavior. SPAN may analyze,
    navigate, and recommend, but it must not mutate platform state directly.
    """

    capability_name: str = "span"
    capability_version: str = "1.0.0"
    advisory_only: bool = True
    minimum_recommendation_confidence: float = 0.70
    maximum_evidence_age: timedelta = timedelta(days=30)
    require_constitutional_assessment: bool = True
    enable_strategic_memory: bool = True
    enabled_spartan_domains: tuple[str, ...] = field(
        default_factory=lambda: (
            "spatial",
            "platform",
            "runtime",
            "architecture",
            "capability",
            "knowledge",
            "governance",
            "standards",
            "research",
            "technology",
            "innovation",
            "forecasting",
            "evolution",
            "constitutional",
            "security",
        )
    )

    def validate(self) -> None:
        if not 0.0 <= self.minimum_recommendation_confidence <= 1.0:
            raise ValueError(
                "minimum_recommendation_confidence must be between 0.0 and 1.0"
            )
        if self.maximum_evidence_age.total_seconds() <= 0:
            raise ValueError("maximum_evidence_age must be positive")
        if not self.capability_name.strip():
            raise ValueError("capability_name must not be empty")
        if not self.capability_version.strip():
            raise ValueError("capability_version must not be empty")
PY

cat > "${SPAN}/models.py" <<'PY'
"""Canonical SPAN™ domain models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Mapping
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RiskLevel(str, Enum):
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class RecommendationPriority(str, Enum):
    OBSERVE = "observe"
    PLANNED = "planned"
    IMPORTANT = "important"
    URGENT = "urgent"
    CONSTITUTIONAL = "constitutional"


class RecommendationStatus(str, Enum):
    PROPOSED = "proposed"
    UNDER_REVIEW = "under_review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DEFERRED = "deferred"
    IMPLEMENTED = "implemented"
    VALIDATED = "validated"


@dataclass(frozen=True, slots=True)
class Evidence:
    source: str
    claim: str
    confidence: float
    observed_at: datetime = field(default_factory=utc_now)
    reference: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Evidence source must not be empty")
        if not self.claim.strip():
            raise ValueError("Evidence claim must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Evidence confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class AnalysisRequest:
    subject: str
    question: str
    requested_by: str
    context: Mapping[str, Any] = field(default_factory=dict)
    request_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("Analysis subject must not be empty")
        if not self.question.strip():
            raise ValueError("Analysis question must not be empty")
        if not self.requested_by.strip():
            raise ValueError("requested_by must not be empty")


@dataclass(frozen=True, slots=True)
class ConstitutionalAssessment:
    aligned: bool
    principles_considered: tuple[str, ...]
    concerns: tuple[str, ...] = ()
    rationale: str = ""
    confidence: float = 1.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Assessment confidence must be between 0.0 and 1.0")
        if not self.principles_considered:
            raise ValueError("At least one constitutional principle is required")


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    request_id: UUID
    summary: str
    findings: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    confidence: float
    risks: tuple[str, ...] = ()
    generated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.summary.strip():
            raise ValueError("Analysis summary must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Analysis confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class NavigationPlan:
    current_state: str
    target_state: str
    steps: tuple[str, ...]
    dependencies: tuple[str, ...] = ()
    risks: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    estimated_effort: str | None = None

    def __post_init__(self) -> None:
        if not self.current_state.strip():
            raise ValueError("current_state must not be empty")
        if not self.target_state.strip():
            raise ValueError("target_state must not be empty")
        if not self.steps:
            raise ValueError("Navigation plan requires at least one step")


@dataclass(frozen=True, slots=True)
class Recommendation:
    title: str
    rationale: str
    analysis: AnalysisResult
    navigation: NavigationPlan
    constitutional_assessment: ConstitutionalAssessment
    priority: RecommendationPriority
    risk_level: RiskLevel
    confidence: float
    status: RecommendationStatus = RecommendationStatus.PROPOSED
    recommendation_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Recommendation title must not be empty")
        if not self.rationale.strip():
            raise ValueError("Recommendation rationale must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Recommendation confidence must be between 0.0 and 1.0")
PY

cat > "${SPAN}/contracts.py" <<'PY'
"""Behavioral contracts for SPAN™ components."""

from __future__ import annotations

from typing import Iterable, Protocol, runtime_checkable
from uuid import UUID

from .models import (
    AnalysisRequest,
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
    Recommendation,
)


@runtime_checkable
class Analyzer(Protocol):
    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Analyze a platform subject and return traceable findings."""


@runtime_checkable
class Navigator(Protocol):
    def navigate(self, analysis: AnalysisResult) -> NavigationPlan:
        """Produce a bounded path from the current state to a target state."""


@runtime_checkable
class ConstitutionalGuide(Protocol):
    def assess(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
    ) -> ConstitutionalAssessment:
        """Assess constitutional alignment before recommendation publication."""


@runtime_checkable
class RecommendationEngine(Protocol):
    def recommend(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
        assessment: ConstitutionalAssessment,
    ) -> Recommendation:
        """Generate a prioritized, constitutionally assessed recommendation."""


@runtime_checkable
class StrategicMemory(Protocol):
    def record(self, recommendation: Recommendation) -> None:
        """Persist recommendation lineage and outcome context."""

    def get(self, recommendation_id: UUID) -> Recommendation | None:
        """Retrieve a recommendation by identifier."""

    def list(self) -> Iterable[Recommendation]:
        """List known recommendations."""


@runtime_checkable
class LifecycleParticipant(Protocol):
    @property
    def is_started(self) -> bool:
        """Return whether the participant is currently started."""

    def start(self) -> None:
        """Start the participant."""

    def stop(self) -> None:
        """Stop the participant."""
PY

cat > "${SPAN}/analyzer.py" <<'PY'
"""Default SPAN™ analyzer."""

from __future__ import annotations

from statistics import fmean
from typing import Iterable

from .models import AnalysisRequest, AnalysisResult, Evidence


class SpectrumPlatformAnalyzer:
    """Evidence-first analyzer for the present platform state.

    Drop 012A supplies a conservative baseline implementation. Future drops
    may compose architecture, runtime, topology, security, and standards
    analyzers through SPARTAN.
    """

    def analyze(
        self,
        request: AnalysisRequest,
        evidence: Iterable[Evidence] = (),
    ) -> AnalysisResult:
        evidence_tuple = tuple(evidence)
        confidence = (
            fmean(item.confidence for item in evidence_tuple)
            if evidence_tuple
            else 0.50
        )

        findings = (
            f"Subject identified: {request.subject}",
            "No specialized analyzer has been attached yet.",
            "Further SPARTAN domain evidence is required for a decisive result.",
        )

        return AnalysisResult(
            request_id=request.request_id,
            summary=f"Baseline analysis completed for {request.subject}.",
            findings=findings,
            evidence=evidence_tuple,
            confidence=confidence,
            risks=("Insufficient specialized evidence may limit precision.",),
        )
PY

cat > "${SPAN}/navigator.py" <<'PY'
"""Default SPAN™ navigator."""

from __future__ import annotations

from .models import AnalysisResult, NavigationPlan


class PlatformNavigator:
    """Creates advisory, reversible platform navigation plans."""

    def navigate(self, analysis: AnalysisResult) -> NavigationPlan:
        return NavigationPlan(
            current_state=analysis.summary,
            target_state="A verified, constitutionally aligned target state.",
            steps=(
                "Collect specialized evidence from relevant SPARTAN domains.",
                "Validate architectural and constitutional constraints.",
                "Model candidate pathways and compare risk.",
                "Submit the preferred pathway for governance review.",
                "Execute only after explicit authorization.",
                "Measure outcomes and preserve the decision record.",
            ),
            dependencies=("SPARTAN domain analysis", "Governance review"),
            risks=analysis.risks,
            success_criteria=(
                "Recommendation is evidence-backed.",
                "Constitutional alignment is explicitly assessed.",
                "Migration is reversible or has a documented recovery path.",
                "Observed outcomes are recorded.",
            ),
        )
PY

cat > "${SPAN}/guidance.py" <<'PY'
"""Constitutional guidance for SPAN™."""

from __future__ import annotations

from .models import (
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
)


class ConstitutionalGuidance:
    """Conservative constitutional assessment.

    This default guide does not claim access to the full Constitutional Graph.
    It checks baseline engineering principles until a platform adapter is wired.
    """

    _BASELINE_PRINCIPLES = (
        "Truth Precedes Intelligence™",
        "Evidence Precedes Knowledge™",
        "Governance Precedes Power™",
        "Stewardship Precedes Optimization™",
        "Human Agency Is Fundamental™",
        "Composition Over Accumulation™",
        "Boundaries Are Constitutional™",
    )

    def assess(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
    ) -> ConstitutionalAssessment:
        concerns: list[str] = []

        if analysis.confidence < 0.70:
            concerns.append("Analysis confidence is below the preferred threshold.")
        if not analysis.evidence:
            concerns.append("No evidence artifacts were attached.")
        if not navigation.success_criteria:
            concerns.append("Navigation plan lacks measurable success criteria.")

        return ConstitutionalAssessment(
            aligned=not concerns,
            principles_considered=self._BASELINE_PRINCIPLES,
            concerns=tuple(concerns),
            rationale=(
                "Baseline constitutional assessment completed. "
                "A Constitutional Graph adapter should replace or augment this "
                "implementation when available."
            ),
            confidence=0.75 if concerns else 0.90,
        )
PY

cat > "${SPAN}/recommendation_engine.py" <<'PY'
"""Strategic recommendation generation for SPAN™."""

from __future__ import annotations

from .models import (
    AnalysisResult,
    ConstitutionalAssessment,
    NavigationPlan,
    Recommendation,
    RecommendationPriority,
    RiskLevel,
)


class StrategicRecommendationEngine:
    """Generates advisory recommendations from validated inputs."""

    def recommend(
        self,
        analysis: AnalysisResult,
        navigation: NavigationPlan,
        assessment: ConstitutionalAssessment,
    ) -> Recommendation:
        confidence = min(
            analysis.confidence,
            assessment.confidence,
        )

        if not assessment.aligned:
            priority = RecommendationPriority.IMPORTANT
            risk_level = RiskLevel.HIGH
            title = "Resolve constitutional concerns before platform evolution"
        elif confidence >= 0.90:
            priority = RecommendationPriority.PLANNED
            risk_level = RiskLevel.LOW
            title = "Proceed to governed implementation planning"
        elif confidence >= 0.70:
            priority = RecommendationPriority.IMPORTANT
            risk_level = RiskLevel.MODERATE
            title = "Strengthen evidence before implementation"
        else:
            priority = RecommendationPriority.OBSERVE
            risk_level = RiskLevel.HIGH
            title = "Defer action pending stronger evidence"

        return Recommendation(
            title=title,
            rationale=(
                f"{analysis.summary} "
                f"Constitutional alignment: {assessment.aligned}. "
                f"Combined confidence: {confidence:.2f}."
            ),
            analysis=analysis,
            navigation=navigation,
            constitutional_assessment=assessment,
            priority=priority,
            risk_level=risk_level,
            confidence=confidence,
        )
PY

cat > "${SPAN}/memory.py" <<'PY'
"""Strategic memory for SPAN™ recommendation lineage."""

from __future__ import annotations

from threading import RLock
from typing import Iterable
from uuid import UUID

from .models import Recommendation


class InMemoryStrategicMemory:
    """Thread-safe reference memory for development and tests.

    Replace with Mammoth™ persistence through an adapter in a later drop.
    """

    def __init__(self) -> None:
        self._items: dict[UUID, Recommendation] = {}
        self._lock = RLock()

    def record(self, recommendation: Recommendation) -> None:
        with self._lock:
            self._items[recommendation.recommendation_id] = recommendation

    def get(self, recommendation_id: UUID) -> Recommendation | None:
        with self._lock:
            return self._items.get(recommendation_id)

    def list(self) -> Iterable[Recommendation]:
        with self._lock:
            return tuple(self._items.values())
PY

cat > "${SPAN}/events.py" <<'PY'
"""SPAN™ domain events."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Mapping
from uuid import UUID, uuid4

from .models import utc_now


class SPANEventType(str, Enum):
    STARTED = "span.started"
    STOPPED = "span.stopped"
    ANALYSIS_COMPLETED = "span.analysis.completed"
    RECOMMENDATION_CREATED = "span.recommendation.created"
    RECOMMENDATION_RECORDED = "span.recommendation.recorded"


@dataclass(frozen=True, slots=True)
class SPANEvent:
    event_type: SPANEventType
    aggregate_id: UUID | None = None
    payload: Mapping[str, Any] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=utc_now)
PY

cat > "${SPAN}/telemetry.py" <<'PY'
"""Minimal telemetry abstraction for SPAN™."""

from __future__ import annotations

from collections import Counter
from threading import RLock
from typing import Mapping


class SPANTelemetry:
    def __init__(self) -> None:
        self._counters: Counter[str] = Counter()
        self._lock = RLock()

    def increment(self, metric: str, value: int = 1) -> None:
        if value < 0:
            raise ValueError("Telemetry increments must be non-negative")
        with self._lock:
            self._counters[metric] += value

    def snapshot(self) -> Mapping[str, int]:
        with self._lock:
            return dict(self._counters)
PY

cat > "${SPAN}/lifecycle.py" <<'PY'
"""Lifecycle management for SPAN™."""

from __future__ import annotations

from threading import RLock


class SPANLifecycle:
    def __init__(self) -> None:
        self._started = False
        self._lock = RLock()

    @property
    def is_started(self) -> bool:
        with self._lock:
            return self._started

    def start(self) -> None:
        with self._lock:
            self._started = True

    def stop(self) -> None:
        with self._lock:
            self._started = False
PY

cat > "${SPAN}/capability.py" <<'PY'
"""SPAN™ composition root at the capability boundary."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .analyzer import SpectrumPlatformAnalyzer
from .config import SPANConfig
from .guidance import ConstitutionalGuidance
from .lifecycle import SPANLifecycle
from .memory import InMemoryStrategicMemory
from .models import AnalysisRequest, Evidence, Recommendation
from .navigator import PlatformNavigator
from .recommendation_engine import StrategicRecommendationEngine
from .telemetry import SPANTelemetry


@dataclass(slots=True)
class SPANCapability:
    """Spectrum Platform Analyzer & Navigator™.

    SPAN is advisory by default. It analyzes, navigates, assesses, recommends,
    and records. It does not mutate AletheusOS™ directly.
    """

    config: SPANConfig
    analyzer: SpectrumPlatformAnalyzer
    navigator: PlatformNavigator
    guidance: ConstitutionalGuidance
    recommendation_engine: StrategicRecommendationEngine
    memory: InMemoryStrategicMemory
    lifecycle: SPANLifecycle
    telemetry: SPANTelemetry
    spartan: object | None = None

    @property
    def name(self) -> str:
        return self.config.capability_name

    @property
    def version(self) -> str:
        return self.config.capability_version

    @property
    def is_started(self) -> bool:
        return self.lifecycle.is_started

    def start(self) -> None:
        self.config.validate()
        if self.spartan is not None and hasattr(self.spartan, "start"):
            self.spartan.start()
        self.lifecycle.start()
        self.telemetry.increment("lifecycle.starts")

    def stop(self) -> None:
        if self.spartan is not None and hasattr(self.spartan, "stop"):
            self.spartan.stop()
        self.lifecycle.stop()
        self.telemetry.increment("lifecycle.stops")

    def evaluate(
        self,
        request: AnalysisRequest,
        evidence: Iterable[Evidence] = (),
    ) -> Recommendation:
        if not self.is_started:
            raise RuntimeError("SPAN must be started before evaluation")

        analysis = self.analyzer.analyze(request, evidence)
        self.telemetry.increment("analysis.completed")

        navigation = self.navigator.navigate(analysis)
        assessment = self.guidance.assess(analysis, navigation)
        recommendation = self.recommendation_engine.recommend(
            analysis,
            navigation,
            assessment,
        )

        if (
            recommendation.confidence
            >= self.config.minimum_recommendation_confidence
        ):
            self.memory.record(recommendation)
            self.telemetry.increment("recommendation.recorded")
        else:
            self.telemetry.increment("recommendation.withheld")

        self.telemetry.increment("recommendation.created")
        return recommendation
PY

cat > "${SPAN}/registry.py" <<'PY'
"""Local registry for SPAN™ components and adapters."""

from __future__ import annotations

from threading import RLock
from typing import Any, Iterable


class SPANRegistry:
    def __init__(self) -> None:
        self._items: dict[str, Any] = {}
        self._lock = RLock()

    def register(self, name: str, component: Any, *, replace: bool = False) -> None:
        normalized = name.strip().lower()
        if not normalized:
            raise ValueError("Registry name must not be empty")

        with self._lock:
            if normalized in self._items and not replace:
                raise KeyError(f"Component already registered: {normalized}")
            self._items[normalized] = component

    def resolve(self, name: str) -> Any:
        normalized = name.strip().lower()
        with self._lock:
            try:
                return self._items[normalized]
            except KeyError as exc:
                raise KeyError(f"Unknown SPAN component: {normalized}") from exc

    def names(self) -> Iterable[str]:
        with self._lock:
            return tuple(sorted(self._items))
PY

cat > "${SPAN}/factory.py" <<'PY'
"""Factory for the SPAN™ capability."""

from __future__ import annotations

from .analyzer import SpectrumPlatformAnalyzer
from .capability import SPANCapability
from .config import SPANConfig
from .guidance import ConstitutionalGuidance
from .lifecycle import SPANLifecycle
from .memory import InMemoryStrategicMemory
from .navigator import PlatformNavigator
from .recommendation_engine import StrategicRecommendationEngine
from .telemetry import SPANTelemetry


def build_span(
    config: SPANConfig | None = None,
    *,
    spartan: object | None = None,
) -> SPANCapability:
    resolved_config = config or SPANConfig()
    resolved_config.validate()

    return SPANCapability(
        config=resolved_config,
        analyzer=SpectrumPlatformAnalyzer(),
        navigator=PlatformNavigator(),
        guidance=ConstitutionalGuidance(),
        recommendation_engine=StrategicRecommendationEngine(),
        memory=InMemoryStrategicMemory(),
        lifecycle=SPANLifecycle(),
        telemetry=SPANTelemetry(),
        spartan=spartan,
    )
PY

cat > "${SPAN}/runtime_adapter.py" <<'PY'
"""Runtime integration adapter for SPAN™.

This module intentionally uses structural typing and defensive reflection so the
drop can coexist with multiple Runtime Registry generations without forcing a
premature dependency on one concrete registry API.
"""

from __future__ import annotations

from typing import Any

from .capability import SPANCapability


def register_span(runtime_registry: Any, span: SPANCapability) -> None:
    """Register SPAN with a compatible runtime registry.

    Supported registry shapes:
    - register(name, component)
    - register(component)
    - register_capability(name, component)
    - register_capability(component)
    """

    attempts = (
        ("register_capability", (span.name, span)),
        ("register_capability", (span,)),
        ("register", (span.name, span)),
        ("register", (span,)),
    )

    for method_name, args in attempts:
        method = getattr(runtime_registry, method_name, None)
        if method is None:
            continue
        try:
            method(*args)
            return
        except TypeError:
            continue

    raise TypeError(
        "Runtime registry is incompatible with the SPAN runtime adapter. "
        "Expected register(...) or register_capability(...)."
    )
PY

cat > "${SPARTAN}/__init__.py" <<'PY'
"""SPARTAN™ — Spatial Platform Analysis Recursive Transformative Autogenous Network™."""

from .domain import (
    DomainAnalysis,
    DomainContext,
    DomainSignal,
    IntelligenceDomain,
)
from .factory import build_spartan
from .network import SPARTANNetwork

__all__ = [
    "DomainAnalysis",
    "DomainContext",
    "DomainSignal",
    "IntelligenceDomain",
    "SPARTANNetwork",
    "build_spartan",
]
PY

cat > "${SPARTAN}/domain.py" <<'PY'
"""Core SPARTAN™ domain contracts and models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, Protocol, runtime_checkable
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True, slots=True)
class DomainSignal:
    domain: str
    signal_type: str
    statement: str
    confidence: float
    source: str
    observed_at: datetime = field(default_factory=utc_now)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("Signal domain must not be empty")
        if not self.signal_type.strip():
            raise ValueError("signal_type must not be empty")
        if not self.statement.strip():
            raise ValueError("Signal statement must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Signal confidence must be between 0.0 and 1.0")


@dataclass(frozen=True, slots=True)
class DomainContext:
    subject: str
    question: str
    state: Mapping[str, Any] = field(default_factory=dict)
    context_id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if not self.subject.strip():
            raise ValueError("Context subject must not be empty")
        if not self.question.strip():
            raise ValueError("Context question must not be empty")


@dataclass(frozen=True, slots=True)
class DomainAnalysis:
    domain: str
    summary: str
    findings: tuple[str, ...]
    signals: tuple[DomainSignal, ...]
    confidence: float
    generated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) -> None:
        if not self.domain.strip():
            raise ValueError("Analysis domain must not be empty")
        if not self.summary.strip():
            raise ValueError("Analysis summary must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Analysis confidence must be between 0.0 and 1.0")


@runtime_checkable
class IntelligenceDomain(Protocol):
    @property
    def name(self) -> str:
        """Canonical domain name."""

    def analyze(self, context: DomainContext) -> DomainAnalysis:
        """Analyze the supplied context and return domain-specific intelligence."""
PY

cat > "${SPARTAN}/domains.py" <<'PY'
"""Reference intelligence domains for SPARTAN™."""

from __future__ import annotations

from dataclasses import dataclass

from .domain import DomainAnalysis, DomainContext


@dataclass(slots=True)
class BaselineIntelligenceDomain:
    """Safe placeholder for a bounded SPARTAN intelligence domain."""

    name: str

    def analyze(self, context: DomainContext) -> DomainAnalysis:
        return DomainAnalysis(
            domain=self.name,
            summary=(
                f"{self.name.title()} intelligence baseline analysis completed "
                f"for {context.subject}."
            ),
            findings=(
                "The domain is registered and operational.",
                "No specialized provider has been attached yet.",
                "Future drops may replace this baseline through adapters.",
            ),
            signals=(),
            confidence=0.50,
        )


DEFAULT_DOMAIN_NAMES: tuple[str, ...] = (
    "spatial",
    "platform",
    "runtime",
    "architecture",
    "capability",
    "knowledge",
    "governance",
    "standards",
    "research",
    "technology",
    "innovation",
    "forecasting",
    "evolution",
    "constitutional",
    "security",
)
PY

cat > "${SPARTAN}/registry.py" <<'PY'
"""Domain registry for SPARTAN™."""

from __future__ import annotations

from threading import RLock
from typing import Iterable

from .domain import IntelligenceDomain


class DomainRegistry:
    def __init__(self) -> None:
        self._domains: dict[str, IntelligenceDomain] = {}
        self._lock = RLock()

    def register(
        self,
        domain: IntelligenceDomain,
        *,
        replace: bool = False,
    ) -> None:
        name = domain.name.strip().lower()
        if not name:
            raise ValueError("Domain name must not be empty")

        with self._lock:
            if name in self._domains and not replace:
                raise KeyError(f"SPARTAN domain already registered: {name}")
            self._domains[name] = domain

    def resolve(self, name: str) -> IntelligenceDomain:
        normalized = name.strip().lower()
        with self._lock:
            try:
                return self._domains[normalized]
            except KeyError as exc:
                raise KeyError(f"Unknown SPARTAN domain: {normalized}") from exc

    def list(self) -> Iterable[IntelligenceDomain]:
        with self._lock:
            return tuple(self._domains[name] for name in sorted(self._domains))

    def names(self) -> Iterable[str]:
        with self._lock:
            return tuple(sorted(self._domains))
PY

cat > "${SPARTAN}/recursive.py" <<'PY'
"""Recursive intelligence cycle for SPARTAN™."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Mapping
from uuid import UUID, uuid4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RecursiveStage(str, Enum):
    OBSERVE = "observe"
    UNDERSTAND = "understand"
    MODEL = "model"
    SIMULATE = "simulate"
    FORECAST = "forecast"
    RECOMMEND = "recommend"
    VALIDATE = "validate"
    LEARN = "learn"
    IMPROVE = "improve"


@dataclass(frozen=True, slots=True)
class RecursiveCycleRecord:
    subject: str
    completed_stages: tuple[RecursiveStage, ...]
    observations: Mapping[str, str] = field(default_factory=dict)
    cycle_id: UUID = field(default_factory=uuid4)
    completed_at: datetime = field(default_factory=utc_now)


class RecursiveIntelligenceCycle:
    """Tracks the canonical SPARTAN recursive cycle.

    Drop 012A records stage progression. Later drops can attach stage handlers,
    simulation providers, model validators, and outcome-learning adapters.
    """

    _ORDER = tuple(RecursiveStage)

    def execute(self, subject: str) -> RecursiveCycleRecord:
        if not subject.strip():
            raise ValueError("Recursive cycle subject must not be empty")

        return RecursiveCycleRecord(
            subject=subject,
            completed_stages=self._ORDER,
            observations={
                stage.value: f"{stage.value.title()} stage completed."
                for stage in self._ORDER
            },
        )
PY

cat > "${SPARTAN}/network.py" <<'PY'
"""SPARTAN™ network composition and orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from statistics import fmean
from threading import RLock
from typing import Iterable

from .domain import DomainAnalysis, DomainContext
from .recursive import RecursiveCycleRecord, RecursiveIntelligenceCycle
from .registry import DomainRegistry


@dataclass(frozen=True, slots=True)
class NetworkAnalysis:
    subject: str
    domain_analyses: tuple[DomainAnalysis, ...]
    recursive_cycle: RecursiveCycleRecord
    confidence: float


@dataclass(slots=True)
class SPARTANNetwork:
    """Distributed recursive intelligence network that powers SPAN™."""

    registry: DomainRegistry
    recursive_cycle: RecursiveIntelligenceCycle
    _started: bool = False
    _lock: RLock = field(default_factory=RLock, repr=False)

    @property
    def name(self) -> str:
        return "spartan"

    @property
    def is_started(self) -> bool:
        with self._lock:
            return self._started

    def start(self) -> None:
        with self._lock:
            self._started = True

    def stop(self) -> None:
        with self._lock:
            self._started = False

    def analyze(
        self,
        context: DomainContext,
        domains: Iterable[str] | None = None,
    ) -> NetworkAnalysis:
        if not self.is_started:
            raise RuntimeError("SPARTAN must be started before analysis")

        selected = (
            tuple(domains)
            if domains is not None
            else tuple(self.registry.names())
        )

        analyses = tuple(
            self.registry.resolve(name).analyze(context)
            for name in selected
        )

        confidence = (
            fmean(item.confidence for item in analyses)
            if analyses
            else 0.0
        )

        return NetworkAnalysis(
            subject=context.subject,
            domain_analyses=analyses,
            recursive_cycle=self.recursive_cycle.execute(context.subject),
            confidence=confidence,
        )
PY

cat > "${SPARTAN}/factory.py" <<'PY'
"""Factory for SPARTAN™."""

from __future__ import annotations

from .domains import BaselineIntelligenceDomain, DEFAULT_DOMAIN_NAMES
from .network import SPARTANNetwork
from .recursive import RecursiveIntelligenceCycle
from .registry import DomainRegistry


def build_spartan(
    enabled_domains: tuple[str, ...] | None = None,
) -> SPARTANNetwork:
    registry = DomainRegistry()

    for name in enabled_domains or DEFAULT_DOMAIN_NAMES:
        registry.register(BaselineIntelligenceDomain(name=name))

    return SPARTANNetwork(
        registry=registry,
        recursive_cycle=RecursiveIntelligenceCycle(),
    )
PY

cat > "${ROOT}/span_bootstrap.py" <<'PY'
"""Convenience bootstrap for SPAN™ and SPARTAN™.

This file avoids modifying the existing runtime composition root. A later
integration drop can wire this bootstrap into the Constitutional Runtime Kernel
after the repository's exact runtime interfaces are inspected.
"""

from __future__ import annotations

from aletheus.strategic.span import SPANConfig, build_span
from aletheus.strategic.spartan import build_spartan


def build_strategic_intelligence(
    config: SPANConfig | None = None,
):
    resolved_config = config or SPANConfig()
    spartan = build_spartan(resolved_config.enabled_spartan_domains)
    span = build_span(resolved_config, spartan=spartan)
    return span
PY

cat > "${TESTS}/test_span_foundation.py" <<'PY'
from aletheus.strategic.span import (
    AnalysisRequest,
    Evidence,
    build_span,
)
from aletheus.strategic.spartan import DomainContext, build_spartan


def test_span_evaluates_and_records_recommendation() -> None:
    spartan = build_spartan()
    span = build_span(spartan=spartan)
    span.start()

    request = AnalysisRequest(
        subject="runtime.core",
        question="Should responsibility be extracted from the composition root?",
        requested_by="test-suite",
    )
    evidence = (
        Evidence(
            source="architecture-review",
            claim="runtime.core has increasing responsibility density",
            confidence=0.92,
        ),
    )

    recommendation = span.evaluate(request, evidence)

    assert recommendation.analysis.request_id == request.request_id
    assert recommendation.confidence >= 0.70
    assert span.memory.get(recommendation.recommendation_id) is not None

    span.stop()
    assert not span.is_started


def test_spartan_runs_registered_domains() -> None:
    network = build_spartan(("architecture", "runtime"))
    network.start()

    result = network.analyze(
        DomainContext(
            subject="AletheusOS",
            question="What should evolve next?",
        )
    )

    assert len(result.domain_analyses) == 2
    assert result.recursive_cycle.completed_stages
    assert result.confidence == 0.50
PY

cat > "${TESTS}/test_span_config.py" <<'PY'
import pytest

from aletheus.strategic.span import SPANConfig


def test_span_config_rejects_invalid_confidence() -> None:
    config = SPANConfig(minimum_recommendation_confidence=1.5)

    with pytest.raises(ValueError):
        config.validate()
PY

cat > "docs_span_architecture.md" <<'MD'
# SPAN™ Architecture

## Canonical identity

**SPAN™**  
Spectrum Platform Analyzer & Navigator™

**SPARTAN™**  
Spatial Platform Analysis Recursive Transformative Autogenous Network™

## Constitutional position

SPAN is the strategic intelligence capability responsible for platform awareness,
analysis, navigation, constitutional guidance, and evidence-backed recommendations.

SPARTAN is the distributed recursive intelligence network operating within SPAN.

## Governing boundaries

1. SPAN is advisory by default.
2. SPAN does not autonomously mutate platform state.
3. Every recommendation carries evidence, confidence, risk, navigation, and
   constitutional assessment.
4. SPARTAN domains remain independently replaceable and evolvable.
5. Strategic memory records recommendation lineage and outcomes.
6. Runtime integration must occur through adapters rather than direct coupling.
7. Capability evolution preserves architectural lineage.

## Recursive cycle

Observe → Understand → Model → Simulate → Forecast → Recommend → Validate →
Learn → Improve → Observe

## Drop 012A scope

This drop establishes:

- Canonical package identities.
- Foundational models and contracts.
- SPAN lifecycle and composition.
- Baseline analyzer, navigator, guidance, recommendation, and memory.
- SPARTAN domain registry and recursive network.
- Defensive runtime registration adapter.
- Tests and bootstrap entry point.

Specialized intelligence, external horizon scanning, persistent Mammoth™ storage,
Constitutional Graph integration, Runtime Registry integration, and Event Bus
publication are intentionally reserved for subsequent drops.
MD

echo
echo "Drop 012A installed."
echo
echo "Created:"
echo "  ${STRATEGIC}/"
echo "  ${ROOT}/span_bootstrap.py"
echo "  ${TESTS}/"
echo "  docs_span_architecture.md"
echo
echo "Recommended validation:"
echo "  python -m compileall ${STRATEGIC} ${ROOT}/span_bootstrap.py"
echo "  pytest -q ${TESTS}"
echo
echo "Next: Engineering Drop 012B — SPAN service pipeline and SPARTAN evidence bridge."
