import importlib


class ProfileLoader:
    """Environment Profiles™ loader."""

    @staticmethod
    def load(profile="development"):
        module = importlib.import_module(f"deployment.{profile}")
        return module.PROFILE
