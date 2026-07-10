"""
Acquisition Models

Genesis 14.16
"""

from dataclasses import dataclass



@dataclass
class AcquisitionDecision:


    asset_id: str

    score: int

    recommendation: str



@dataclass
class AcquisitionMission:


    name: str

    rules: dict

