# prefiq/core/logger.py
from __future__ import annotations
import logging, sys
from typing import Optional
from prefiq.settings.get_settings import load_settings

class PrefiqLogger:
    _configured = False

    @classmethod
    def configure(cls, force: bool = False) -> None:
        if cls._configured and not force:
            return
        s = load_settings()
        level = getattr(logging, s.LOG_LEVEL.upper(), logging.INFO)
        fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt))
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

# global default logger (no need for parentheses)
log: logging.Logger = get_logger()
