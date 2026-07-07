from .models import IntentRecord


class IntentRegistry:
    def __init__(self):
        self.records: dict[str, IntentRecord] = {}

    def register(self, record: IntentRecord):
        self.records[record.id] = record
        return record

    def all(self):
        return list(self.records.values())

    def get(self, intent_id: str):
        return self.records.get(intent_id)

    def count(self):
        return len(self.records)
