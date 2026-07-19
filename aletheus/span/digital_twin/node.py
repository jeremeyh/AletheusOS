from dataclasses import dataclass, field

@dataclass
class TwinNode:
    identifier:str
    kind:str
    metadata:dict=field(default_factory=dict)
