class CandidateQueue:
    """Queue for normalized Scout™ candidates."""

    def __init__(self):
        self.items = []

    def add_many(self, items):
        self.items.extend(items)

    def all(self):
        return self.items

    def high_priority(self, minimum=8.0):
        return [x for x in self.items if getattr(x, "scout_score", 0) >= minimum]
