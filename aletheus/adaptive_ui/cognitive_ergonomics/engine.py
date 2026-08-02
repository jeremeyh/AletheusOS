from .models import *


class Engine:
    def policy(self, state, density):
        if state == CognitiveState.OVERLOADED:
            return {
                "whitespaceScale": 1.4,
                "animationScale": 0.4,
                "secondaryPanels": "COLLAPSE",
                "notificationMode": "MUTE_NON_CRITICAL",
            }
        if state == CognitiveState.CRITICAL:
            return {
                "whitespaceScale": 1.0,
                "animationScale": 0.2,
                "secondaryPanels": "HIDE",
                "notificationMode": "CRITICAL_ONLY",
            }
        return {
            "whitespaceScale": 1.0,
            "animationScale": 1.0,
            "secondaryPanels": "PRESERVE",
            "notificationMode": "NORMAL",
        }
