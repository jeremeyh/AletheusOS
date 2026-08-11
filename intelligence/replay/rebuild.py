"""
Rebuild Projections
"""

from core.bootstrap import bootstrap
from intelligence.replay.replay_engine import replay_engine

bootstrap.boot()

count = replay_engine.replay()

print()

print("Replay Complete")

print("Events Processed:", count)
