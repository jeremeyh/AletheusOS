"""
Card Hawk Security Engine

Genesis 14.18
"""


from .identity import IdentityManager
from .audit import AuditEngine
from .fraud import FraudEngine



class SecurityEngine:


    def __init__(self):

        self.identity = IdentityManager()

        self.audit = AuditEngine()

        self.fraud = FraudEngine()



    def protect(
        self,
        action
    ):


        return {

            "secured":

                True

        }

