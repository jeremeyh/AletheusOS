"""
Card Hawk Intelligence Gateway

Genesis 13.2

Application boundary between Card Hawk
and AletheusOS intelligence services.
"""


from .routing import IntelligenceRouter
from .models import (
    IntelligenceRequest,
    IntelligenceResponse
)


class CardHawkIntelligenceGateway:


    def __init__(
        self,
        runtime=None
    ):

        self.runtime = runtime

        self.router = IntelligenceRouter()



    def evaluate(
        self,
        request: IntelligenceRequest
    ):

        capabilities = (
            self.router.resolve(
                request.operation
            )
        )


        return IntelligenceResponse(

            decision="ANALYSIS_READY",

            confidence=0,

            reasoning={

                "asset":
                    request.asset_id,

                "required_capabilities":
                    capabilities

            }

        )


