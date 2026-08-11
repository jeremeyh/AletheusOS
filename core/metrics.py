"""
CardHawk OS™
Runtime Metrics
"""


class Metrics:
    def __init__(self):

        self.values = {}

    def increment(self, key):

        self.values[key] = self.values.get(key, 0) + 1

    def record(self, key, value):

        self.values[key] = value

    def snapshot(self):

        return dict(self.values)


metrics = Metrics()
