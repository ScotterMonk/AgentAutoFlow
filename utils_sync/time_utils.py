"""Time/interval formatting utilities.

This module is intentionally UI-agnostic (no tkinter imports) so it can be used by
both the GUI and tests without requiring a display environment.
"""


def format_duration_hms(total_seconds) -> str:
    """Format a duration as `##h:##m:##s`.

    Examples:
        5 -> "00h:00m:05s"
        65 -> "00h:01m:05s"
        3661 -> "01h:01m:01s"
    """

    try:
        total = int(float(total_seconds))
    except Exception:
        total = 0

    if total < 0:
        total = 0

    hours, rem = divmod(total, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours:02d}h:{minutes:02d}m:{seconds:02d}s"

