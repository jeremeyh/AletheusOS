"""
CardHawk OS™
Event Store Reader
"""

import json
from pathlib import Path

LOG = Path("logs/events.jsonl")


def read_events():

    if not LOG.exists():
        return []

    events = []

    with LOG.open() as fp:
        for line in fp:
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    return events
