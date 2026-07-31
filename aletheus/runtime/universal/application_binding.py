"""
Application Binding Layer

Genesis 91.5
"""


class ApplicationBinding:
    def bind(self, application):

        return {"application": application, "runtime": "AletheusOS", "status": "bound"}
