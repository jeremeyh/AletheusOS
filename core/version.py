"""
CardHawk OS™
Platform Version Information
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    codename: str
    build: str

    @property
    def short(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @property
    def full(self):
        return (
            f"CardHawk OS™ "
            f"{self.major}.{self.minor}.{self.patch} "
            f"({self.codename}) "
            f"Build {self.build}"
        )


VERSION = Version(
    major=10,
    minor=0,
    patch=0,
    codename="Repository Consolidation",
    build=datetime.utcnow().strftime("%Y.%m.%d"),
)


def get_version():
    return VERSION.full


def get_build():
    return VERSION.build
