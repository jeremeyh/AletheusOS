from dataclasses import dataclass,field
from datetime import datetime
@dataclass
class Metric:
    name:str
    value:float|int|str
    timestamp:str=field(default_factory=lambda:datetime.utcnow().isoformat())
class Telemetry:
    _metrics=[]
    @classmethod
    def record(cls,name,value):
        m=Metric(name,value);cls._metrics.append(m);return m
    @classmethod
    def latest(cls): return cls._metrics
