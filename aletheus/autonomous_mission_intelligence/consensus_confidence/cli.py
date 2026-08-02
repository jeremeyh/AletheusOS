from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    AgentRecommendation,
)


def main() -> None:
    recommendation = AgentRecommendation("agent-demo", "PROCEED", 0.9)
    result = Engine().aggregate([recommendation])
    print(dumps(result, indent=2, sort_keys=True))
