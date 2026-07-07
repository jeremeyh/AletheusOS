from .models import ReleaseCertification


class ReleaseCertificationReporter:
    def render(self, cert: ReleaseCertification) -> str:
        return f"""
========================================================
ALETHEUSOS RELEASE CERTIFICATION
========================================================

Certification......................{cert.status}

Platform Health Score..............{cert.health_score}%

Git Working Tree Clean.............{"PASS" if cert.git_clean else "FAIL"}

Summary
{cert.summary}

Timestamp
{cert.created_at}

========================================================
""".strip()
