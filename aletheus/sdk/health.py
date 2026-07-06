from .core import aletheus_sdk


def health():
    return aletheus_sdk.health()
