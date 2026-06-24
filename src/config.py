"""Configuration loading and run-context resolution.

Everything the pipeline needs is derived from ``config.yaml`` + ``outlets.yaml``
+ the current clock, so a run is reproducible from those two files and a date.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import yaml

# Project root = parent of the ``src`` package directory.
ROOT = Path(__file__).resolve().parent.parent

_LOG = logging.getLogger("vnnews")


def _read_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_config(path: str | Path | None = None) -> dict[str, Any]:
    """Load ``config.yaml`` (defaults to the one at the project root)."""
    cfg_path = Path(path) if path else ROOT / "config.yaml"
    cfg = _read_yaml(cfg_path)
    cfg["_root"] = ROOT
    return cfg


def load_outlets(path: str | Path | None = None) -> dict[str, Any]:
    """Load ``outlets.yaml`` (the outlet registry)."""
    out_path = Path(path) if path else ROOT / "outlets.yaml"
    return _read_yaml(out_path)


def resolve_path(cfg: dict[str, Any], key: str) -> Path:
    """Resolve a configured (possibly relative) path against the project root."""
    raw = cfg["paths"][key]
    p = Path(raw)
    return p if p.is_absolute() else ROOT / p


def ensure_dirs(cfg: dict[str, Any]) -> None:
    """Create all output/cache directories declared in config."""
    for key in (
        "raw_html",
        "raw_feeds",
        "robots_cache",
        "processed",
        "reports_dir",
        "figures_dir",
    ):
        resolve_path(cfg, key).mkdir(parents=True, exist_ok=True)


@dataclass(frozen=True)
class Window:
    """The collection window, as timezone-aware bounds in the project tz."""

    start: datetime
    end: datetime
    tz: ZoneInfo

    def contains(self, dt: datetime | None) -> bool:
        """True if ``dt`` falls within [start, end]. None is treated as unknown -> False."""
        if dt is None:
            return False
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=self.tz)
        return self.start <= dt <= self.end


def resolve_window(cfg: dict[str, Any], now: datetime | None = None) -> Window:
    """Compute the snapshot window from config.

    Explicit ``window.start`` / ``window.end`` (ISO dates) win; otherwise the
    window is the last ``window.days_back`` days ending now (project tz).
    """
    tz = ZoneInfo(cfg["project"]["timezone"])
    now = now or datetime.now(tz)
    wcfg = cfg.get("window", {})
    start_s, end_s = wcfg.get("start"), wcfg.get("end")
    if start_s and end_s:
        start = datetime.fromisoformat(str(start_s)).replace(tzinfo=tz)
        end = datetime.fromisoformat(str(end_s)).replace(tzinfo=tz)
    else:
        days = int(wcfg.get("days_back", 21))
        end = now
        # Start at the beginning of the day, ``days`` back, to capture full days.
        start = (now - timedelta(days=days)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
    return Window(start=start, end=end, tz=tz)


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configure root logging once and return the project logger."""
    logging.basicConfig(
        level=getattr(logging, str(level).upper(), logging.INFO),
        format="%(asctime)s %(levelname)-7s %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    return _LOG
