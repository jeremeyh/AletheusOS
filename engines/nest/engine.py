from aletheus.runtime.context import AletheusContext

ENGINE_NAME = "NEST™"
ENGINE_DESCRIPTION = "Intelligence observation and nesting layer."


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
