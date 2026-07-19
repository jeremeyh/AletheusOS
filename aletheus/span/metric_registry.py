from __future__ import annotations
from collections import defaultdict
from .metrics import Metric

class MetricRegistry:
    def __init__(self):
        self._metrics=[]
    def add(self,m:Metric):
        self._metrics.append(m)
    def all(self):
        return tuple(self._metrics)
    def by_category(self):
        d=defaultdict(list)
        for m in self._metrics:
            d[m.category].append(m)
        return dict(d)
