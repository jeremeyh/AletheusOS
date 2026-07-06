from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from aletheus.intent_runtime.models import Intent


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RuntimeContext:
    """
    Universal runtime context for AletheusOS.

    Every execution carries:
        • Request metadata
        • Payload
        • Intent
        • Results
        • Execution trace
        • Diagnostics

    The RuntimeContext is passed between engines,
    services, governance, and runtime components.
    """

    # ------------------------------------------------------------------
    # Core Request
    # ------------------------------------------------------------------

    command: str

    payload: Dict[str, Any] = field(default_factory=dict)

    application: str = "system"

    founder: str = "Founder"

    request_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    created_at: str = field(default_factory=utc_now)

    # ------------------------------------------------------------------
    # Intent
    # ------------------------------------------------------------------

    intent: Optional[Intent] = None

    # ------------------------------------------------------------------
    # Runtime Data
    # ------------------------------------------------------------------

    results: Dict[str, Any] = field(default_factory=dict)

    metadata: Dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    errors: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)

    execution_trace: List[Dict[str, Any]] = field(
        default_factory=list
    )

    # ------------------------------------------------------------------
    # Results
    # ------------------------------------------------------------------

    def add_result(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.results[key] = value

    # ------------------------------------------------------------------
    # Diagnostics
    # ------------------------------------------------------------------

    def add_error(
        self,
        error: Any,
    ) -> None:

        self.errors.append(str(error))

    def add_warning(
        self,
        warning: Any,
    ) -> None:

        self.warnings.append(str(warning))

    # ------------------------------------------------------------------
    # Trace
    # ------------------------------------------------------------------

    def add_trace(
        self,
        stage: str,
        detail: Any,
    ) -> None:

        self.execution_trace.append(
            {
                "stage": stage,
                "detail": detail,
                "timestamp": utc_now(),
            }
        )

    # ------------------------------------------------------------------
    # Runtime Helpers
    # ------------------------------------------------------------------

    @property
    def has_intent(self) -> bool:
        return self.intent is not None

    @property
    def has_errors(self) -> bool:
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    def clear_results(self) -> None:
        self.results.clear()

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:

        return {
            "request_id": self.request_id,
            "command": self.command,
            "application": self.application,
            "founder": self.founder,
            "created_at": self.created_at,
            "payload": self.payload,
            "intent": (
                self.intent.intent_id
                if self.intent
                else None
            ),
            "results": self.results,
            "errors": self.errors,
            "warnings": self.warnings,
            "execution_trace": self.execution_trace,
            "metadata": self.metadata,
        }


# ----------------------------------------------------------------------
# Canonical Runtime Alias
# ----------------------------------------------------------------------

AletheusContext = RuntimeContext

