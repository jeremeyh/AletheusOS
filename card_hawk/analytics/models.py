"""
Analytics Models

Genesis 14.19
"""

from dataclasses import dataclass


@dataclass
class Metric:
    name: str

    value: float


@dataclass
class Report:
    title: str

    data: dict
