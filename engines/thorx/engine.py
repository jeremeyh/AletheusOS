from aletheus.runtime.context import AletheusContext

ENGINE_NAME = "THORᵡ"
ENGINE_DESCRIPTION = "Trading Heuristic Opportunity Rating engine"


class ThorX:
    """
    Backward-compatible THORᵡ engine.
    Older code expects a ThorX class.
    Newer runtime can continue using run().
    """

    @staticmethod
    def run(context: AletheusContext) -> AletheusContext:
        context.add_result(
            ENGINE_NAME,
            {
                "status": "online",
                "description": ENGINE_DESCRIPTION,
                "payload_received": getattr(context, "payload", None),
            },
        )
        return context


def run(context: AletheusContext) -> AletheusContext:
    """
    Functional entry point.
    """
    return ThorX.run(context)
