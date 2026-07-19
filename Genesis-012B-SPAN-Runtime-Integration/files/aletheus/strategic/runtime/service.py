"""Lifecycle-safe runtime facade for SPAN."""

from __future__ import annotations

from time import perf_counter
from typing import Any, Mapping

from aletheus.strategic.span import build_span
from aletheus.strategic.spartan import build_spartan

from .models import RuntimeCapabilityStatus, StrategicProposalEnvelope


class SPANRuntimeService:
    """Compose SPAN/SPARTAN with existing AletheusOS runtime authorities."""

    service_name = "span"
    version = "012B"

    def __init__(
        self,
        *,
        events: Any | None = None,
        telemetry: Any | None = None,
        ledger: Any | None = None,
        council: Any | None = None,
        span_factory: Any = build_span,
        spartan_factory: Any = build_spartan,
    ) -> None:
        self._events = events
        self._telemetry = telemetry
        self._ledger = ledger
        self._council = council
        self._span_factory = span_factory
        self._spartan_factory = spartan_factory
        self._span: Any | None = None
        self._spartan: Any | None = None
        self._status = RuntimeCapabilityStatus.CREATED
        self._last_error: str | None = None

    @property
    def status(self) -> RuntimeCapabilityStatus:
        return self._status

    @property
    def span(self) -> Any:
        if self._span is None:
            raise RuntimeError("SPAN has not been initialized")
        return self._span

    @property
    def spartan(self) -> Any:
        if self._spartan is None:
            raise RuntimeError("SPARTAN has not been initialized")
        return self._spartan

    def initialize(self) -> "SPANRuntimeService":
        if self._status in {
            RuntimeCapabilityStatus.INITIALIZED,
            RuntimeCapabilityStatus.RUNNING,
        }:
            return self
        try:
            self._span = self._span_factory()
            self._spartan = self._spartan_factory()
            self._status = RuntimeCapabilityStatus.INITIALIZED
            self._emit("StrategicCapabilityInitialized", self.health())
            return self
        except Exception as exc:
            self._fail(exc)
            raise

    def start(self) -> "SPANRuntimeService":
        if self._status is RuntimeCapabilityStatus.CREATED:
            self.initialize()
        if self._status is RuntimeCapabilityStatus.RUNNING:
            return self
        if self._status is RuntimeCapabilityStatus.FAILED:
            raise RuntimeError("Cannot start a failed SPAN service")
        self._status = RuntimeCapabilityStatus.RUNNING
        self._emit("StrategicCapabilityStarted", self.health())
        return self

    def stop(self) -> "SPANRuntimeService":
        if self._status is RuntimeCapabilityStatus.STOPPED:
            return self
        self._status = RuntimeCapabilityStatus.STOPPED
        self._emit("StrategicCapabilityStopped", self.health())
        return self

    def health(self) -> dict[str, Any]:
        return {
            "name": self.service_name,
            "version": self.version,
            "status": self._status.value,
            "span_ready": self._span is not None,
            "spartan_ready": self._spartan is not None,
            "last_error": self._last_error,
        }

    def submit_proposal(
        self,
        *,
        title: str,
        summary: str,
        evidence: tuple[Mapping[str, Any], ...] = (),
        confidence: float = 0.0,
    ) -> StrategicProposalEnvelope:
        if self._status is not RuntimeCapabilityStatus.RUNNING:
            raise RuntimeError("SPAN runtime service must be running")

        started = perf_counter()
        proposal = StrategicProposalEnvelope(
            title=title,
            summary=summary,
            evidence=evidence,
            confidence=confidence,
        )
        record = proposal.as_record()

        if self._ledger is not None:
            self._ledger.append({"type": "strategic_proposal", **record})
        if self._council is not None:
            self._council.submit(record)

        self._emit("StrategicRecommendationCreated", record)
        self._increment("span.proposals.created")
        self._observe("span.proposals.latency_seconds", perf_counter() - started)
        return proposal

    def _emit(self, event_type: str, payload: Mapping[str, Any]) -> None:
        if self._events is not None:
            self._events.publish(event_type, payload)

    def _increment(self, metric: str, value: int = 1) -> None:
        if self._telemetry is not None:
            self._telemetry.increment(metric, value)

    def _observe(self, metric: str, value: float) -> None:
        if self._telemetry is not None:
            self._telemetry.observe(metric, value)

    def _fail(self, exc: Exception) -> None:
        self._last_error = f"{type(exc).__name__}: {exc}"
        self._status = RuntimeCapabilityStatus.FAILED
        self._emit("StrategicCapabilityFailed", self.health())
        self._increment("span.failures")
