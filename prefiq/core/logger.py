# prefiq/core/logger.py
from __future__ import annotations
import logging, sys
from typing import Optional
from prefiq.settings.get_settings import load_settings

# ANSI color codes (both level-keys and generic color names)
_COLORS = {
    # level colors
    "DEBUG": "\033[36m",     # Cyan
    "INFO": "\033[32m",      # Green
    "WARNING": "\033[33m",   # Yellow
    "ERROR": "\033[31m",     # Red
    "CRITICAL": "\033[41m",  # Red background

    # generic colors
    "green": "\033[32m",
    "red": "\033[31m",
    "yellow": "\033[33m",
    "cyan": "\033[36m",
    "magenta": "\033[35m",
    "grey": "\033[90m",

    # parts
    "TIME": "\033[90m",      # Grey
    "NAME": "\033[35m",      # Magenta

    # reset
    "RESET": "\033[0m",
}

def colorize(text: str, color: str) -> str:
    """
    Colorize arbitrary text. `color` may be a generic color ('green', 'red', ...)
    or a log level name ('INFO', 'ERROR', ...).
    """
    c = _COLORS.get(color, "")
    r = _COLORS["RESET"]
    return f"{c}{text}{r}" if c else text

def badge(ok: bool) -> str:
    """Return a green check or red cross."""
    return "✅" if ok else "❌"

def banner(text: str, *, color: str = "cyan", blank_before: bool = True) -> str:
    """
    Build a section header string, optionally preceded by a blank line,
    and colored (default cyan).
    """
    b = colorize(text, color)
    return f"\n{b}" if blank_before else b

def okc(text: str) -> str:
    """Green colored text (success)."""
    return colorize(text, "green")

def failx(text: str) -> str:
    """Red colored text (error)."""
    return colorize(text, "red")

class ColorFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        levelname = record.levelname
        color = _COLORS.get(levelname, "")
        reset = _COLORS["RESET"]

        # timestamp in grey, level colored, logger name in magenta
        asctime = self.formatTime(record, self.datefmt)
        time_str = f"{_COLORS['TIME']}{asctime}{reset}"
        level_str = f"{color}{levelname:<8}{reset}"
        name_str = f"{_COLORS['NAME']}{record.name}{reset}"
        msg = record.getMessage()
        return f"{time_str} [{level_str}] {name_str}: {msg}"

class PrefiqLogger:
    _configured = False

    @classmethod
    def configure(cls, force: bool = False) -> None:
        if cls._configured and not force:
            return
        s = load_settings()
        level = getattr(logging, s.LOG_LEVEL.upper(), logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorFormatter())
        root = logging.getLogger()
        root.setLevel(level)
        root.handlers.clear()
        root.addHandler(handler)
        cls._configured = True

    @classmethod
    def get(cls, name: Optional[str] = None) -> logging.Logger:
        cls.configure()
        s = load_settings()
        base = s.LOG_NAMESPACE or "prefiq"
        logger_name = f"{base}{('.' + name) if name else ''}"
        return logging.getLogger(logger_name)

# function form
def get_logger(name: Optional[str] = None) -> logging.Logger:
    return PrefiqLogger.get(name)

# global default logger
log: logging.Logger = get_logger()

__all__ = [
    "get_logger", "log",
    "colorize", "banner", "okc", "failx", "badge",
]
