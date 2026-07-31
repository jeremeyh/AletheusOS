"""
Card Hawk Security Engine

Genesis 14.18
"""

from .audit import AuditEngine
from .fraud import FraudEngine
from .identity import IdentityManager


class SecurityEngine:
    def __init__(self):

        self.identity = IdentityManager()

        self.audit = AuditEngine()

        self.fraud = FraudEngine()

    def protect(self, action):

        return {"secured": True}
