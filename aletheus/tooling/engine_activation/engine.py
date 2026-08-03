from __future__ import annotations

import json
from pathlib import Path
from typing import Any, ClassVar

from .models import EngineState


class ActivationManager:
    VALID_TRANSITIONS: ClassVar[dict[str, set[str]]] = {
        "registered": {"starting"},
        "starting": {"active", "failed"},
        "active": {"stopping", "failed"},
        "stopping": {"stopped", "failed"},
        "stopped": {"starting"},
        "failed": {"starting", "stopped"},
    }

    def __init__(self, registry: Path, output: Path) -> None:
        self.registry = registry
        self.output = output
        self.states: dict[str, EngineState] = {}

    def load(self) -> None:
        payload = json.loads(self.registry.read_text(encoding="utf-8"))
        for item in payload.get("engines", []):
            if not isinstance(item, dict):
                continue
            name = str(item.get("engine_name"))
            self.states[name] = EngineState(
                engine_name=name,
                lifecycle="registered",
                active=False,
            )

    def transition(self, engine_name: str, target: str) -> EngineState:
        state = self.states[engine_name]
        allowed = self.VALID_TRANSITIONS.get(state.lifecycle, set())
        if target not in allowed:
            raise ValueError(
                f"Invalid transition for {engine_name}: {state.lifecycle} -> {target}"
            )
        state.lifecycle = target
        state.active = target == "active"
        state.generation += 1
        return state

    def activate_all(self) -> dict[str, Any]:
        if not self.states:
            self.load()
        activated = []
        failed = []
        for name in sorted(self.states):
            try:
                self.transition(name, "starting")
                state = self.transition(name, "active")
                activated.append(state.to_dict())
            except (RuntimeError, ValueError, TypeError, LookupError, OSError) as exc:
                failed.append({"engine_name": name, "error": type(exc).__name__})
        report = {
            "activated": activated,
            "failed": failed,
            "activated_count": len(activated),
            "failed_count": len(failed),
        }
        self.output.mkdir(parents=True, exist_ok=True)
        (self.output / "engine-activation-state.json").write_text(
            json.dumps(report, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return report
