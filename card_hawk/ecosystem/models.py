"""
Ecosystem Models

Genesis 14.21
"""

from dataclasses import dataclass


@dataclass
class Partner:
    name: str

    trust_score: int


@dataclass
class Extension:
    name: str

    developer: str
