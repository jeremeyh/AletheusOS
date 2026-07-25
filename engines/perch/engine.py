from aletheus.runtime.context import AletheusContext

ENGINE_NAME = "PERCH™"
ENGINE_DESCRIPTION = "Marketplace watch and observation engine."
def run(context: AletheusContext) -> AletheusContext:
    context.add_result(ENGINE_NAME, {"status":"online","description":ENGINE_DESCRIPTION,"payload_received":context.payload})
    return context
