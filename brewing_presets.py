"""Brewing-timer presets shared by the desktop Timer tab (main.py) and the web timer (web/app.py -> /api/timer).

Pure data, no GUI imports. Each preset: (tea type, seconds).
"""
TIMER_PRESETS = [
    ("Green Tea", 180),
    ("Black Tea", 300),
    ("Oolong", 240),
    ("White Tea", 240),
    ("Pu-erh", 300),
]


def preset_label(name: str, seconds: int) -> str:
    """'Green Tea (3 min)' -- the button text used by the desktop timer."""
    return f"{name} ({seconds // 60} min)"
