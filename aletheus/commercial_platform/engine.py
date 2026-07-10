"""
Commercial Intelligence Engine

Genesis 13.45
"""


from .subscriptions import SubscriptionEngine
from .entitlements import EntitlementEngine
from .usage import UsageMeter
from .billing import BillingEngine
from .analytics import CommercialAnalytics



class CommercialPlatformEngine:


    def __init__(self):

        self.subscriptions = SubscriptionEngine()

        self.entitlements = EntitlementEngine()

        self.usage = UsageMeter()

        self.billing = BillingEngine()

        self.analytics = CommercialAnalytics()



    def authorize(
        self,
        subscription,
        capability
    ):


        return self.entitlements.check(

            subscription,

            capability

        )

