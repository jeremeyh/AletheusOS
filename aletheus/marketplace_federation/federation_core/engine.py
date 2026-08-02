from __future__ import annotations

from typing import Any

from .models import Request


class Engine:
    VERSION = "31.0.0"

    def dispatch(self, request: Request) -> dict[str, Any]:
        if not request.request_id.strip():
            raise ValueError("request_id cannot be empty")
        return {
            "status": "ACCEPTED",
            "version": self.VERSION,
            "spartanGate": "REQUIRED",
            "constitutionalGate": "REQUIRED",
        }
