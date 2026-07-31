"""
Founder Dashboard Engine

Genesis 13.32
"""


class FounderDashboard:
    def __init__(self):

        self.widgets = []

    def register(self, widget):

        self.widgets.append(widget)

    def snapshot(self):

        return [
            {"name": widget.name, "status": widget.status} for widget in self.widgets
        ]
