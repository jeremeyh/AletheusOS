"""
Notification Priority Engine

Genesis 13.19
"""


class NotificationPriorityEngine:
    def classify(self, event):

        confidence = event.confidence

        if confidence >= 90:
            return "critical"

        if confidence >= 70:
            return "high"

        if confidence >= 40:
            return "normal"

        return "low"
