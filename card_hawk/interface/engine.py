"""
Card Hawk Cognitive Interface Router

Genesis 60.7
"""


from .intent_classifier import IntentClassifier
from .request_router import RequestRouter


class CognitiveInterfaceRouter:


    def __init__(self):

        self.classifier = IntentClassifier()

        self.router = RequestRouter()



    def initialize(self):

        return {

            "system":

            "card_hawk_cognitive_interface_router",


            "status":

            "operational",


            "genesis":

            "60.7"

        }



    def interpret(self, request):

        intent = self.classifier.classify(
            request
        )


        destination = self.router.route(
            intent
        )


        return {


            "request":

            request,


            "intent":

            intent,


            "route":

            destination,


            "status":

            "classified"


        }

