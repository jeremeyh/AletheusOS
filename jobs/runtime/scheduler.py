from datetime import datetime

from jobs.runtime.manager import JobManager


class JobScheduler:
    _jobs = []

    @classmethod
    def register(cls, name, func):
        cls._jobs.append(
            {
                "name": name,
                "func": func,
            }
        )

    @classmethod
    def run_all(cls):

        results = []

        for job in cls._jobs:

            status = "SUCCESS"

            started = datetime.now()

            try:

                job["func"]()

            except Exception as e:

                status = "FAILED"

                error = str(e)

            completed = datetime.now()

            record = {
                "job": job["name"],
                "status": status,
                "started": started.isoformat(timespec="seconds"),
                "completed": completed.isoformat(timespec="seconds"),
            }

            if status == "FAILED":
                record["error"] = error

            JobManager.record(record)

            results.append(record)

        return results

    @classmethod
    def jobs(cls):
        return cls._jobs

    @classmethod
    def count(cls):
        return len(cls._jobs)
