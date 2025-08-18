# prefiq/log/logger.py

from __future__ import annotations

import json
import logging
import os
import sys
from typing import Any, Dict, Optional, Set

# ---------- helpers ----------

def _std_record_fields() -> Set[str]:
    """All standard LogRecord attributes to exclude from extras."""
    return set(vars(logging.LogRecord("", 0, "", 0, "", (), None)).keys())

_STD_FIELDS = _std_record_fields()


# ---------- formatters ----------

class JsonFormatter(logging.Formatter):
    """Simple JSON formatter (level, logger, message, time + extras)."""
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "time": self.formatTime(record, datefmt="%Y-%m-%dT%H:%M:%S%z"),
        }
        # include extras (anything set on the record that isn't standard)
        for key, value in record.__dict__.items():
            if key not in _STD_FIELDS:
                payload[key] = value
        return json.dumps(payload, ensure_ascii=False)


class TextFormatter(logging.Formatter):
    """
    Produces: "YYYY-MM-DD HH:MM:SS [LEVEL] short.logger | message key=value ..."
    - Colors by level (INFO green, WARNING yellow, ERROR red, etc.)
    - Trims the configured base namespace from logger names.
    - Renders record.extra fields as key=value tail.
    """
    COLORS = {
        "DEBUG":    "\033[36m",        # cyan
        "INFO":     "\033[32m",        # green
        "WARNING":  "\033[33m",        # yellow
        "ERROR":    "\033[31m",        # red
        "CRITICAL": "\033[41m\033[97m" # white on red background
    }
    RESET = "\033[0m"

    def __init__(self, base_ns: Optional[str] = None, use_color: bool = True):
        super().__init__(datefmt="%Y-%m-%d %H:%M:%S")
        self.base_ns = (base_ns or "").strip() or None
        self.use_color = use_color

    def _short_name(self, full: str) -> str:
        if not self.base_ns:
            return full
        if full == self.base_ns:
            return full.split(".")[-1]
        prefix = self.base_ns + "."
        return full[len(prefix):] if full.startswith(prefix) else full

    def format(self, record: logging.LogRecord) -> str:
        ts = self.formatTime(record, self.datefmt)
        name = self._short_name(record.name)
        msg = record.getMessage()

        # Render extras as key=value
        extras = []
        for k, v in record.__dict__.items():
            if k in _STD_FIELDS:
                continue
            if isinstance(v, (str, int, float, bool)) or v is None:
                extras.append(f"{k}={v!s}")
            else:
                extras.append(f"{k}={repr(v)}")
        tail = (" " + " ".join(extras)) if extras else ""

        level = record.levelname
        if self.use_color and level in self.COLORS:
            level_str = f"{self.COLORS[level]}{level}{self.RESET}"
        else:
            level_str = level

        return f"{ts} [{level_str}] {name} | {msg}{tail}"


# ---------- config & API ----------

def _should_color(explicit: Optional[str]) -> bool:
    """
    Decide whether to colorize:
    - explicit "true"/"1" enables color
    - explicit "false"/"0" disables color
    - otherwise: auto (enabled only if stdout is a TTY)
    """
    if explicit is None or explicit.strip().lower() == "auto":
        return sys.stdout.isatty()
    val = explicit.strip().lower()
    if val in ("1", "true", "yes", "on"):
        return True
    if val in ("0", "false", "no", "off"):
        return False
    return sys.stdout.isatty()

def configure_logging(
    level: str = "INFO",
    fmt: str = "json",
    base_logger: str = "prefiq",
    color: Optional[str] = None,  # "auto" | "true" | "false"
) -> logging.Logger:
    """
    Configure a base logger and return it. Children under this namespace inherit the handler.
    Pass `color` as "auto"/"true"/"false" for text mode coloring.

    IMPORTANT: If logging is already configured (e.g., via dictConfig),
    this function will NO-OP to avoid overwriting handlers/filters.
    """
    base_ns = (base_logger or "prefiq").strip() or "prefiq"

    # ---- NEW: do not override an existing configuration ----
    root = logging.getLogger()
    if root.handlers or logging.getLogger(base_ns).handlers:
        return logging.getLogger(base_ns)
    # --------------------------------------------------------

    # Normalize inputs
    level_name = (level or "INFO").upper()
    fmt_name = (fmt or "json").lower()

    logger = logging.getLogger(base_ns)
    logger.setLevel(getattr(logging, level_name, logging.INFO))
    logger.propagate = False

    # Clear existing handlers (avoid duplicates on reload)
    for h in list(logger.handlers):
        logger.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)

    if fmt_name == "json":
        handler.setFormatter(JsonFormatter())
    else:
        use_color = _should_color(color or os.getenv("LOG_COLOR", "auto"))
        handler.setFormatter(TextFormatter(base_ns=base_ns, use_color=use_color))

    logger.addHandler(handler)

    # Quiet root to avoid duplicate logs if someone logs to root accidentally
    root.setLevel(logging.ERROR)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a named logger. For consistent formatting/namespace trimming,
    ensure the name is under the configured base namespace (e.g., 'prefiq.settings').
    """
    return logging.getLogger(name)
