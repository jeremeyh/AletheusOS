"""
Notification Routing Engine

Genesis 13.19
"""


class NotificationRouter:


    def route(
        self,
        priority
    ):


        routes = {


            "critical":

            [

                "dashboard",

                "mobile",

                "email"

            ],



            "high":

            [

                "dashboard",

                "mobile"

            ],



            "normal":

            [

                "dashboard"

            ],



            "low":

            []

        }


        return routes.get(
            priority,
            []
        )

