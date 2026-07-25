import os


class SecretsManager:
    """Secure secrets loading helper."""

    @staticmethod
    def get(name, default=None):
        return os.getenv(name, default)
