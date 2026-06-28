class DeploymentProfiles:
    """7.0G — Deployment Profiles™."""

    PROFILES = {
        "local": {
            "name": "Local Development",
            "debug": True,
            "background_jobs": False,
            "live_providers": False,
            "logging_level": "DEBUG",
        },
        "demo": {
            "name": "Demo",
            "debug": False,
            "background_jobs": False,
            "live_providers": False,
            "logging_level": "INFO",
        },
        "testing": {
            "name": "Testing",
            "debug": True,
            "background_jobs": False,
            "live_providers": False,
            "logging_level": "DEBUG",
        },
        "production": {
            "name": "Production",
            "debug": False,
            "background_jobs": True,
            "live_providers": True,
            "logging_level": "WARNING",
        },
    }

    @classmethod
    def get(cls, profile):
        return cls.PROFILES.get(profile, cls.PROFILES["local"])

    @classmethod
    def all(cls):
        return cls.PROFILES
