"""
Commercial Intelligence Engine

Genesis 13.45
"""

from .analytics import CommercialAnalytics
from .billing import BillingEngine
from .entitlements import EntitlementEngine
from .subscriptions import SubscriptionEngine
from .usage import UsageMeter


class CommercialPlatformEngine:
    def __init__(self):

        self.subscriptions = SubscriptionEngine()

        self.entitlements = EntitlementEngine()

        self.usage = UsageMeter()

        self.billing = BillingEngine()

        self.analytics = CommercialAnalytics()

    def authorize(self, subscription, capability):

        return self.entitlements.check(subscription, capability)
