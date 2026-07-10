# Genesis 8 Command Dispatcher

A production-oriented dispatcher foundation for AletheusOS.

## Runtime path

1. Immutable registry lookup
2. Request type validation
3. Global middleware
4. Per-command middleware
5. Sync or async handler invocation
6. Result type validation
7. Normalized dispatch errors

## Install and test

```bash
python -m pip install -e ".[test]"
pytest -q
```

## Basic usage

```python
registry = CompiledCommandRegistry(commands)
dispatcher = CommandDispatcher(registry)

result = await dispatcher.dispatch(
    "workflow.execute",
    request,
    context=CommandContext(actor_id="user-123"),
)
```

This package intentionally does not perform reflection. Reflection belongs in
the bootstrap compiler, which should emit `CompiledCommand` objects consumed by
this dispatcher.
