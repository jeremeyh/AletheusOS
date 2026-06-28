"""
Replay Journal
"""

import json
from pathlib import Path

LOG = Path("logs/events.jsonl")


def replay():

    if not LOG.exists():

        return []

    rows=[]

    with LOG.open() as fp:

        for line in fp:

            rows.append(json.loads(line))

    return rows
