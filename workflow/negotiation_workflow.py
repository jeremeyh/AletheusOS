class NegotiationWorkflow:
    """Offer negotiation helper."""
    def __init__(self):
        self.history=[]

    def record_offer(self, amount, note=''):
        self.history.append({'offer':amount,'note':note})

    def accepted(self, amount):
        self.history.append({'accepted':amount})

    def rejected(self, amount):
        self.history.append({'rejected':amount})
