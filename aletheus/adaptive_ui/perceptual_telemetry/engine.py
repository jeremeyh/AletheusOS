from .models import *


class Engine:
    def classify(self, t):
        t = t.clamped()
        if t.system_urgency >= 0.9:
            return CognitiveState.CRITICAL
        if t.cognitive_load >= 0.8:
            return CognitiveState.OVERLOADED
        if t.focus_depth >= 0.75 and t.intent_velocity >= 0.5:
            return CognitiveState.FOCUSED
        if t.intent_velocity < 0.3:
            return CognitiveState.EXPLORING
        return CognitiveState.CALM
