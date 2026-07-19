"""Runtime integration adapter for SPAN™.

This module intentionally uses structural typing and defensive reflection so the
drop can coexist with multiple Runtime Registry generations without forcing a
premature dependency on one concrete registry API.
"""

from __future__ import annotations

from typing import Any

from .capability import SPANCapability


def register_span(runtime_registry: Any, span: SPANCapability) -> None:
    """Register SPAN with a compatible runtime registry.

    Supported registry shapes:
    - register(name, component)
    - register(component)
    - register_capability(name, component)
    - register_capability(component)
    """

    attempts = (
        ("register_capability", (span.name, span)),
        ("register_capability", (span,)),
        ("register", (span.name, span)),
        ("register", (span,)),
    )

    for method_name, args in attempts:
        method = getattr(runtime_registry, method_name, None)
        if method is None:
            continue
        try:
            method(*args)
            return
        except TypeError:
            continue

    raise TypeError(
        "Runtime registry is incompatible with the SPAN runtime adapter. "
        "Expected register(...) or register_capability(...)."
    )
