from datetime import datetime


def sample_events():

    now = datetime.now().strftime("%H:%M:%S")

    return [
        {
            "icon": "📥",
            "title": "Asset Imported",
            "description": "Caleb Williams uploaded.",
            "timestamp": now,
        },
        {
            "icon": "🦅",
            "title": "Hawk A•Eye™",
            "description": "OCR extraction complete.",
            "timestamp": now,
        },
        {
            "icon": "🧠",
            "title": "Founder AI™",
            "description": "Card identified.",
            "timestamp": now,
        },
        {
            "icon": "⚡",
            "title": "THORᵡ",
            "description": "Score: 81.7",
            "timestamp": now,
        },
        {
            "icon": "💰",
            "title": "Marketplace",
            "description": "4 comps discovered.",
            "timestamp": now,
        },
        {
            "icon": "🧬",
            "title": "Portfolio",
            "description": "Digital Twin updated.",
            "timestamp": now,
        },
        {
            "icon": "✅",
            "title": "Asset Saved",
            "description": "Vault synchronized.",
            "timestamp": now,
        },
    ]
