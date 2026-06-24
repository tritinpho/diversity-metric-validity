"""Timezone-aware datetime parsing/formatting, normalized to the project tz.

Vietnamese outlets emit dates in inconsistent formats:
  - VnExpress  RSS: ``Tue, 23 Jun 2026 11:43:58 +0700``      (RFC-822)
  - Nhan Dan   RSS: ``Tue, 23 Jun 2026 12:00:01 +07:00``     (RFC-822, colon offset)
  - Tuoi Tre   RSS: ``6/23/2026 10:58:00 AM``                (US M/D/Y, tz-naive)
  - sitemaps:       ``2026-06-23T12:00:01+07:00``            (ISO-8601)

We parse all of them with dateutil and normalize to Asia/Ho_Chi_Minh. A tz-naive
timestamp is assumed to already be in local (VN) time, which is the correct
assumption for these domestic outlets.
"""
from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from dateutil import parser as _dtparser

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


def parse_dt(raw: str | None, tz: ZoneInfo = VN_TZ) -> datetime | None:
    """Parse a heterogeneous date string to a tz-aware datetime in ``tz``.

    Returns None if ``raw`` is empty or unparseable. tz-naive inputs are
    localized to ``tz`` (assumed already local); tz-aware inputs are converted.
    """
    if not raw or not str(raw).strip():
        return None
    try:
        dt = _dtparser.parse(str(raw))
    except (ValueError, OverflowError, TypeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def to_iso(dt: datetime | None) -> str | None:
    """ISO-8601 string for a datetime (None -> None)."""
    return dt.isoformat() if dt is not None else None


def now(tz: ZoneInfo = VN_TZ) -> datetime:
    """Current time in the project tz."""
    return datetime.now(tz)
