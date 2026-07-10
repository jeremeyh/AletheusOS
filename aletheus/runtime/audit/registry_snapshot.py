from __future__ import annotations


def registry_snapshot(runtime):
    """
    Genesis 6 Runtime Registry inspection.

    Provides SPA visibility into
    registered capabilities.
    """

    registry = getattr(
        runtime,
        "registry",
        None,
    )

    if registry is None:
        return {
            "available": False,
            "reason": "Runtime registry unavailable",
        }


    data = {}

    for key, value in vars(registry).items():
        if not key.startswith("_"):
            data[key] = value


    return {
        "available": True,
        "type": registry.__class__.__name__,
        "entries": data,
        "entry_count": len(data),
    }
