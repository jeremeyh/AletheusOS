"""
Episodic Memory

Genesis 13.28
"""

from .models import MemoryRecord


class EpisodicMemory:
    def remember(self, event):

        return MemoryRecord(memory_id="episode", memory_type="episodic", content=event)
