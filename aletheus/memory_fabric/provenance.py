"""
Memory Provenance

Genesis 13.47
"""


class MemoryProvenance:
    def attach(self, record, source):

        record.provenance = {"source": source}

        return record
