from datetime import UTC, datetime, timedelta


def get_timestamp(seconds: int = 0, minutes: int = 0, hours: int = 0) -> int:
    dt = datetime.now(UTC) + timedelta(seconds=seconds, minutes=minutes, hours=hours)
    return int(dt.timestamp())
