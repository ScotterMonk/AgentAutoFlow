from utils_sync.time_utils import format_duration_hms


def test_format_duration_hms_zero() -> None:
    assert format_duration_hms(0) == "00h:00m:00s"


def test_format_duration_hms_seconds() -> None:
    assert format_duration_hms(5) == "00h:00m:05s"


def test_format_duration_hms_minutes_seconds() -> None:
    assert format_duration_hms(65) == "00h:01m:05s"


def test_format_duration_hms_hours_minutes_seconds() -> None:
    assert format_duration_hms(3661) == "01h:01m:01s"


def test_format_duration_hms_negative_is_clamped() -> None:
    assert format_duration_hms(-1) == "00h:00m:00s"


def test_format_duration_hms_float_is_truncated() -> None:
    assert format_duration_hms(5.9) == "00h:00m:05s"

