class JobManager:

    _history = []

    @classmethod
    def record(cls, job_record):

        cls._history.append(job_record)

    @classmethod
    def history(cls):

        return list(reversed(cls._history))

    @classmethod
    def clear(cls):

        cls._history.clear()

    @classmethod
    def count(cls):

        return len(cls._history)
