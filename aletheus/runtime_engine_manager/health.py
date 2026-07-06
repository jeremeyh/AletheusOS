from .core import runtime_engine_manager


def health():
    return runtime_engine_manager.health()
