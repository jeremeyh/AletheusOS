"""
Mission Scheduling Engine

Genesis 13.25
"""


class MissionScheduler:
    def __init__(self):

        self.jobs = []

    def schedule(self, mission, frequency):

        self.jobs.append({"mission": mission, "frequency": frequency})

        return self.jobs
