from aletheus.runtime.builder import RuntimeBuilder

runtime = (
    RuntimeBuilder()
    .development()
    .plugins(True)
    .enterprise(False)
    .clustered(False)
    .build()
)

print("========================================================")
print("ALETHEUSOS RUNTIME BUILDER")
print("========================================================")
print()

for key, value in runtime.items():
    if key == "container":
        print(f"{key:<15}: RuntimeContainer")
    else:
        print(f"{key:<15}: {value}")

print()
print("========================================================")

# BEGIN ALETHEUSOS BUILDER STUDIO CONSUMER SEAM
_BUILDER_STUDIO_ALLOWED_OPERATIONS = frozenset(('development', 'enterprise', 'clustered', 'plugins', 'build'))


def dispatch_builder_operation(operation, *args, **kwargs):
    """Dispatch an authorized Builder Studio operation to RuntimeBuilder.

    This is a narrow consumer seam over the existing RuntimeBuilder authority.
    Unknown operations fail closed.
    """
    if operation not in _BUILDER_STUDIO_ALLOWED_OPERATIONS:
        raise ValueError(
            f"Unsupported Builder Studio operation: {operation!r}"
        )

    builder = RuntimeBuilder()
    target = getattr(builder, operation, None)

    if target is None or not callable(target):
        raise RuntimeError(
            f"RuntimeBuilder operation is unavailable: {operation!r}"
        )

    return target(*args, **kwargs)
# END ALETHEUSOS BUILDER STUDIO CONSUMER SEAM
