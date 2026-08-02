from __future__ import annotations

from json import dumps

from .engine import Engine
from .models import (
    TimelineTask,
)


def main() -> None:
    task = TimelineTask("task-demo", 1.0)
    result = Engine().optimize([task])
    print(dumps(result, indent=2, sort_keys=True))
