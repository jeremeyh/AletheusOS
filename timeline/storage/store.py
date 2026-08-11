"""
CardHawk OS™
Timeline Store
"""

import json
from pathlib import Path

TIMELINE_FILE = Path("data/timeline.json")

TIMELINE_FILE.parent.mkdir(parents=True, exist_ok=True)


class TimelineStore:
    def load(self):

        if not TIMELINE_FILE.exists():
            return []

        with TIMELINE_FILE.open() as fp:
            return json.load(fp)

    def save(self, timeline):

        with TIMELINE_FILE.open("w") as fp:
            json.dump(timeline, fp, indent=2)


store = TimelineStore()
