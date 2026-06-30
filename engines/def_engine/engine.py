from aletheus.context import AletheusContext
ENGINE_NAME = "DEF"
ENGINE_DESCRIPTION = "Decision Engine Framework."
def run(context: AletheusContext) -> AletheusContext:
    context.add_result(ENGINE_NAME, {"status":"online","description":ENGINE_DESCRIPTION,"payload_received":context.payload})
    return context
