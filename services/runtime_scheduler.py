from __future__ import annotations

from collections.abc import Callable
from typing import Any

from services.context import utc_now_iso


class RuntimeScheduler:
    def __init__(self) -> None:
        self.jobs: dict[str, dict[str, Any]] = {}

    def register(self, name: str, description: str, handler: Callable[[], Any]) -> None:
        self.jobs[name] = {"description": description, "handler": handler, "last_run": None, "last_result": None}

    def run(self, name: str) -> Any:
        if name not in self.jobs:
            return {"error": f"Unknown job: {name}"}
        result = self.jobs[name]["handler"]()
        self.jobs[name]["last_run"] = utc_now_iso()
        self.jobs[name]["last_result"] = result
        return result

    def list_jobs(self) -> dict[str, dict[str, Any]]:
        return {k: {"description": v["description"], "last_run": v["last_run"], "last_result": v["last_result"]} for k, v in self.jobs.items()}
