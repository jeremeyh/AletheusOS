"""
Universal Intelligence Layer Adapter.

Provides a bounded orchestration facade over Aletheus reasoning, executive,
semantic, memory, event, and workspace capabilities.
"""

from __future__ import annotations

from typing import Any, Dict


class UniversalIntelligenceAdapter:
    """Composes existing intelligence services without duplicating them."""

    version = "1.6.0-compat"

    def __init__(self, runtime: Any) -> None:
        self.runtime = runtime

    def context(
        self,
        question: str = "",
        supplied_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        runtime = self.runtime

        context = {
            "question": question,
            "runtime": {
                "version": getattr(runtime, "version", "unknown"),
                "status": (
                    "online"
                    if getattr(runtime, "booted", False)
                    else "offline"
                ),
            },
            "reasoning": runtime.reasoning.stats(),
            "executive": runtime.executive.stats(),
            "semantic": runtime.semantic.stats(),
            "memory": runtime.memory.stats(),
            "workspace": runtime.workspace.stats(),
            "recent_events": runtime.events.recent(limit=10),
        }

        if supplied_context:
            context["supplied_context"] = supplied_context

        return context

    def reason(
        self,
        question: str,
        supplied_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        context = self.context(
            question=question,
            supplied_context=supplied_context,
        )

        return self.runtime.reasoning.evaluate(
            question=question,
            runtime=self.runtime,
            context=context,
        )

    def synthesize(
        self,
        question: str,
        supplied_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        context = self.context(
            question=question,
            supplied_context=supplied_context,
        )

        reasoning = self.runtime.reasoning.evaluate(
            question=question,
            runtime=self.runtime,
            context=context,
        )

        concepts = self.runtime.semantic.search_concepts(
            query=question,
        )

        assertions = self.runtime.semantic.query_assertions()

        return {
            "question": question,
            "context": context,
            "reasoning": reasoning,
            "concepts": concepts,
            "assertions": assertions,
        }

    def decide(
        self,
        question: str,
        supplied_context: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:
        context = self.context(
            question=question,
            supplied_context=supplied_context,
        )

        return self.runtime.reasoning.decision(
            question=question,
            runtime=self.runtime,
            context=context,
        )

    def brief(self) -> Dict[str, Any]:
        return self.runtime.executive.daily_brief(
            self.runtime,
        )

    def snapshot(self) -> Dict[str, Any]:
        return {
            "executive": self.runtime.executive.snapshot(
                self.runtime,
            ),
            "context": self.context(),
        }

    def timeline(self, limit: int = 50) -> Dict[str, Any]:
        return {
            "events": self.runtime.events.recent(limit=limit),
            "memory": self.runtime.memory.recall(limit=limit),
        }

    def stats(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": "operational",
            "services": {
                "reasoning": self.runtime.reasoning.stats(),
                "executive": self.runtime.executive.stats(),
                "semantic": self.runtime.semantic.stats(),
                "memory": self.runtime.memory.stats(),
                "workspace": self.runtime.workspace.stats(),
            },
        }
