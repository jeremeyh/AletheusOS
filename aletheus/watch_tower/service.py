from .integrity_engine import IntegrityEngine


class WatchTowerService:
    authority="Watch Tower™"
    family="Platform Intelligence"
    knows="Repository Integrity"
    def __init__(self):
        self.engine=IntegrityEngine()
    def verify(self):
        return self.engine.evaluate()
