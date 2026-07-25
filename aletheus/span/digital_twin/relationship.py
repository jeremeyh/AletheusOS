from dataclasses import dataclass


@dataclass(frozen=True)
class Relationship:
    source:str
    target:str
    relation:str
