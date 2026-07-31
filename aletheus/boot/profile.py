from dataclasses import dataclass


@dataclass(frozen=True)
class BootProfile:
    name: str
    load_ui: bool = False
    load_apps: bool = False
    safe_mode: bool = False
    developer_mode: bool = False


PROFILES = {
    "sdk": BootProfile(name="sdk"),
    "developer": BootProfile(name="developer", developer_mode=True),
    "founder": BootProfile(
        name="founder", load_ui=True, load_apps=True, developer_mode=True
    ),
    "production": BootProfile(name="production", load_apps=True),
    "headless": BootProfile(name="headless"),
    "safe": BootProfile(name="safe", safe_mode=True),
    "recovery": BootProfile(name="recovery", safe_mode=True),
}


def resolve_profile(name: str) -> BootProfile:
    return PROFILES.get(name, PROFILES["developer"])
