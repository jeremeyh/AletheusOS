"""
Anchor Evolution Strategic Planning Engine

Genesis 8.25

Creates long-term evolution roadmaps.
"""


import time
import uuid


class AnchorStrategicPlanningEngine:


    def __init__(
        self,
        analytics,
        intelligence,
        research
    ):

        self.analytics = analytics
        self.intelligence = intelligence
        self.research = research

        self.plans = []



    def create_plan(
        self,
        anchors
    ):

        analytics = (
            self.analytics
            .analyze()
        )


        opportunities = (
            self.research
            .generate_proposals(
                anchors
            )
        )


        priorities = (
            self.rank_priorities(
                opportunities
            )
        )


        plan = {

            "plan_id":
                str(uuid.uuid4()),

            "trajectory":
                analytics["trajectory"],

            "priorities":
                priorities,

            "created":
                time.time()

        }


        self.plans.append(
            plan
        )


        return plan



    def rank_priorities(
        self,
        opportunities
    ):

        ranked = []


        for item in opportunities:

            priority = (
                item.get(
                    "priority",
                    "normal"
                )
            )


            score = {

                "critical":100,

                "high":75,

                "normal":50

            }.get(
                priority,
                25
            )


            ranked.append({

                "anchor":
                    item["anchor"],

                "priority":
                    priority,

                "score":
                    score

            })


        return sorted(

            ranked,

            key=lambda x:
                x["score"],

            reverse=True

        )



    def roadmap(self):

        return self.plans



    def snapshot(self):

        return {

            "plan_count":
                len(self.plans)

        }
