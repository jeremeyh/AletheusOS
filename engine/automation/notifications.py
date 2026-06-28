def notification_payload(title: str, body: str, channel: str = "app") -> dict:
    return {"title": title, "body": body, "channel": channel}
