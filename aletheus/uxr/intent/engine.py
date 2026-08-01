from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Intent:
    name: str
    layout_type: str
    data_density: str
    capabilities: tuple[str, ...]
    confidence: float


class Engine:
    def translate(
        self, prompt: str, *, user_role: str = "user", device: str = "desktop"
    ) -> Intent:
        p = prompt.lower()
        if any(x in p for x in ("compare", "versus", "roi", "acquisition")):
            n, l, c = (
                "compare_and_evaluate",
                "dashboard",
                ("Evidence", "Knowledge", "Risk", "Predictive", "Reason"),
            )
        elif any(x in p for x in ("configure", "settings", "setup")):
            n, l, c = "configure", "workflow", ("Knowledge", "Policy")
        elif any(x in p for x in ("audit", "review", "history")):
            n, l, c = "audit", "detail", ("Evidence", "Memory", "Governance")
        else:
            n, l, c = "summarize", "summary", ("Knowledge", "Reason")
        d = (
            "compact"
            if device == "mobile"
            else ("executive" if user_role in {"executive", "c_level"} else "dense")
        )
        return Intent(n, l, d, c, 0.93)
