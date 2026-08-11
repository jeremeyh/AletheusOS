from aletheus.context import AletheusContext

ENGINE_NAME = "THORᵡ"
ENGINE_DESCRIPTION = "Trading Heuristic Opportunity Rating engine."


def run(context: AletheusContext) -> AletheusContext:
    context.add_result(
        ENGINE_NAME,
        {
            "status": "online",
            "description": ENGINE_DESCRIPTION,
            "payload_received": context.payload,
        },
    )
    return context
