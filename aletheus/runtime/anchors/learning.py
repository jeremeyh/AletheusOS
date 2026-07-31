"""
Anchor Learning Memory Engine

Genesis 8.13

Stores institutional runtime knowledge.
"""

import time


class AnchorLearningMemory:
    def __init__(self):

        self.memories = []

    def record(self, anchor, event, outcome, metadata=None):

        memory = {
            "anchor": anchor,
            "event": event,
            "outcome": outcome,
            "metadata": metadata or {},
            "timestamp": time.time(),
        }

        self.memories.append(memory)

        return memory

    def history(self, anchor=None):

        if anchor:
            return [item for item in self.memories if item["anchor"] == anchor]

        return self.memories

    def successful_patterns(self):

        return [item for item in self.memories if item["outcome"] == "success"]

    def failed_patterns(self):

        return [item for item in self.memories if item["outcome"] == "failure"]

    def recommendations(self, anchor):

        failures = [
            item
            for item in self.memories
            if (item["anchor"] == anchor and item["outcome"] == "failure")
        ]

        if failures:
            return {
                "recommendation": "investigate",
                "reason": "historical failures detected",
            }

        return {"recommendation": "continue", "reason": "healthy history"}

    def snapshot(self):

        return {
            "memory_count": len(self.memories),
            "successful": len(self.successful_patterns()),
            "failed": len(self.failed_patterns()),
        }
