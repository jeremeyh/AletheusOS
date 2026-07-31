"""
Card Hawk Protection Engine

Genesis 14.26
"""

from .appraisal import AppraisalEngine
from .insurance import InsuranceEngine
from .registry import AssetRegistry


class ProtectionEngine:
    def __init__(self):

        self.registry = AssetRegistry()

        self.appraisal = AppraisalEngine()

        self.insurance = InsuranceEngine()

    def protect(self, asset):

        return {"status": "protected"}
