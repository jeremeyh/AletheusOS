from __future__ import annotations

from typing import Any

from .models import A3yeResponse


class Engine:
    SUPPORTED = frozenset(
        {
            "A3YE_CONVERSATION",
            "AXIOMUX_FIELD",
            "EXECUTIVE_REPORT",
            "TECHNICAL_REPORT",
            "STATISTICAL_APPENDIX",
            "DASHBOARD",
            "PRESENTATION",
            "SPREADSHEET",
            "VOICE",
            "API",
        }
    )

    def hydrate(
        self, response: A3yeResponse, requested: tuple[str, ...]
    ) -> dict[str, Any]:
        invalid = [item for item in requested if item not in self.SUPPORTED]
        if invalid:
            raise ValueError(f"Unsupported projections: {invalid}")
        return {
            "responseId": response.response_id,
            "thesis": response.thesis,
            "determination": response.determination.__dict__,
            "projections": list(requested),
            "projectionNeutralityPreserved": True,
            "uxrReady": True,
            "axiomUXReady": True,
            "voiceReady": "VOICE" in requested or "A3YE_CONVERSATION" in requested,
        }
