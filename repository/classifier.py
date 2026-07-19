from .models import RepositoryDomain
class RepositoryClassifier:
    def classify(self,p):
        return RepositoryDomain.SOURCE if p.startswith('aletheus/') else RepositoryDomain.UNKNOWN
