def build_alert(title: str, message: str, severity: str = "info") -> dict:
    return {"title": title, "message": message, "severity": severity}
