from datetime import datetime, timezone


def as_utc(dt: datetime | None) -> datetime | None:
    """
    naive → aware(UTC) または既に aware なら UTC へ変換
    """
    if dt is None:
        return None
    return (
        dt.replace(tzinfo=timezone.utc)
        if dt.tzinfo is None
        else dt.astimezone(timezone.utc)
    )


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
