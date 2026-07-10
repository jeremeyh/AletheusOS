from __future__ import annotations

from aletheus.execution_engine import execution_engine


class AletheusSDK:
    """
    Public SDK for AletheusOS.

    Applications should interact with the platform through this
    interface rather than importing internal engines directly.
    """

    GENESIS = "26.0"
    VERSION = "1.0.0"

    def execute(
        self,
        *,
        identity: str,
        application: str,
        query: str,
    ):
        return execution_engine.execute(
            identity=identity,
            application=application,
            query=query,
        )

    def health(self):
        return {
            "name": "Aletheus SDK",
            "genesis": self.GENESIS,
            "version": self.VERSION,
            "status": "healthy",
        }


#
# Canonical SDK singleton
#
aos = AletheusSDK()

#
# Backwards compatibility alias.
#
# Older Genesis modules import:
#
#     from aletheus.sdk.core import aletheus_sdk
#
# Keep the alias until the architecture reconciliation
# is complete.
#
aletheus_sdk = aos
