"""
CardHawk OS™
Execution Trace
"""

import json
from pathlib import Path

LOG = Path("logs/events.jsonl")


def trace():

    if not LOG.exists():
        print("No events.")
        return

    with LOG.open() as fp:

        for line in fp:

            e = json.loads(line)

            print()

            print("Timestamp      :", e.get("timestamp", "N/A"))
            print("Event          :", e.get("event", "N/A"))
            print("Source         :", e.get("source", "Legacy Event"))
            print("Correlation ID :", e.get("correlation_id", "Legacy"))
            print("Payload        :", e.get("payload", {}))
