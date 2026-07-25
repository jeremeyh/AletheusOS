from __future__ import annotations

from plugins.base_plugin import BasePlugin
from services.context import PipelineContext


class Plugin(BasePlugin):
    name = "PERCH™"
    version = "1.0.0"
    description = "Observation and watchlist intelligence layer."

    def execute(self, context: PipelineContext) -> PipelineContext:
        price = float(context.payload.get("price", 0) or 0)
        context.add_result("PERCH", {
            "status": "observed",
            "watch_signal": "active" if price else "passive",
            "market_posture": "monitor",
            "notes": "PERCH scanned the opportunity/watchlist state."
        })
        return context
