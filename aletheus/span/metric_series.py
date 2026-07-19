class MetricSeries:
    def __init__(self):
        self.snapshots=[]
    def add(self,snapshot):
        self.snapshots.append(snapshot)
