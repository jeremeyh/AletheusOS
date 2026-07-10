"""
Genesis 8.89
Wisdom Accumulation Engine
"""


class WisdomAccumulationEngine:


    def __init__(self):

        self.wisdom=[]



    def accumulate(self, experience):

        record={

            "experience":
                experience,

            "converted_to_wisdom":
                True

        }


        self.wisdom.append(record)

        return record
