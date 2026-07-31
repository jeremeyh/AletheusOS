"""
Automation Scheduler

Genesis 13.42
"""


class AutomationScheduler:
    def __init__(self):

        self.jobs = []

    def schedule(self, workflow, frequency):

        self.jobs.append({"workflow": workflow, "frequency": frequency})

        return self.jobs
