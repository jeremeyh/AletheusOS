"""
Memory Storage Layer

Genesis 13.28
"""


class MemoryStorage:


    def __init__(self):

        self.records = []



    def store(
        self,
        record
    ):

        self.records.append(
            record
        )



    def query(
        self,
        memory_type=None
    ):

        if not memory_type:

            return self.records


        return [

            r

            for r

            in self.records

            if r.memory_type == memory_type

        ]

