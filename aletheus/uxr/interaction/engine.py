from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Event:
    trigger: str
    node_id: str
    payload: dict[str, Any]


class Engine:
    def dispatch(self, event: Event) -> dict[str, object]:
        accepted = event.trigger in {"onSelect", "onSubmit", "onChange"}
        return {
            "accepted": accepted,
            "actionType": "DISPATCH_INTENT" if accepted else "NO_OP",
            "nodeId": event.node_id,
            "payload": event.payload,
        }
