"""
API Gateway Models

Genesis 13.43
"""

from dataclasses import dataclass


@dataclass
class APIRequest:
    identity: str

    capability: str

    payload: dict


@dataclass
class APIResponse:
    success: bool

    data: dict
