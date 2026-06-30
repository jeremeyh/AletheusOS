from __future__ import annotations

from services.context import PipelineContext
from plugins.base_plugin import BasePlugin


class Plugin(BasePlugin):
    name = "TALON™"
    version = "1.0.0"
    description = "Acquisition execution framework."

    def execute(self, context: PipelineContext) -> PipelineContext:
        price = float(context.payload.get("price", 0) or 0)
        suggested_offer = round(price * 0.82, 2) if price else 0
        context.add_result("TALON", {
            "status": "armed",
            "suggested_offer": suggested_offer,
            "execution_mode": "offer" if price else "research",
            "notes": "TALON prepared acquisition execution guidance."
        })
        return context
