from __future__ import annotations

from aletheus.span.span_engine import SpanEngine


class PipelineRunner:
    """Runs the complete SPAN orchestration."""

    def __init__(self):
        self.engine = SpanEngine()

    def execute(self):
        # Placeholder orchestration until providers/analyzers
        # are fully wired into the runtime.
        return {
            "engine": self.engine.run(),
            "status": "ok",
        }
