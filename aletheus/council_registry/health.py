from .core import council_engine_registry


def health():
    return council_engine_registry.health()
