"""
Security Models

Genesis 14.18
"""

from dataclasses import dataclass


@dataclass
class SecurityEvent:


    event_type: str

    actor: str

    authorized: bool



@dataclass
class Policy:


    name: str

    enabled: bool

