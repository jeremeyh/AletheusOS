from .change import Change

class DriftEngine:
    def compare(self, previous, current):
        changes=[]
        keys=set(previous.metrics)|set(current.metrics)
        for k in sorted(keys):
            p=float(previous.metrics.get(k,0))
            c=float(current.metrics.get(k,0))
            d=round(c-p,4)
            trend="stable"
            if d>0:
                trend="up"
            elif d<0:
                trend="down"
            changes.append(Change(k,p,c,d,trend))
        return changes
