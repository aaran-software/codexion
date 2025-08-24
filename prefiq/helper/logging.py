# prefiq/helper/logging.py

import sys
import os
from time import strftime, localtime

# ANSI colors (work on most terminals). Disable with NO_COLOR=1
_COLORS = {
    "DEBUG": "\033[36m",     # cyan
    "INFO": "\033[32m",      # green
    "WARNING": "\033[33m",   # yellow
    "ERROR": "\033[31m",     # red
    "CRITICAL": "\033[41m",  # red background
}
_RESET = "\033[0m"

_LEVELS = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}
_level = _LEVELS["INFO"]
_use_color = not os.environ.get("NO_COLOR")
_stream = sys.stdout

def set_level(level_name: str) -> None:
    """Set minimum level to print: DEBUG, INFO, WARNING, ERROR, CRITICAL"""
    global _level
    _level = _LEVELS.get(level_name.upper(), _LEVELS["INFO"])

def set_stream(stream) -> None:
    """Redirect output (e.g., to a file)."""
    global _stream
    _stream = stream

def _emit(level: str, message: str) -> None:
    if _LEVELS[level] < _level:
        return
    ts = strftime("%Y-%m-%d %H:%M:%S", localtime())
    lvl = level
    if _use_color and _stream.isatty():
        color = _COLORS.get(level, "")
        lvl = f"{color}{level}{_RESET}"
    _stream.write(f"{ts} [{lvl}] {message}\n")
    _stream.flush()

def debug(msg: str):    _emit("DEBUG", msg)
def info(msg: str):     _emit("INFO", msg)
def warning(msg: str):  _emit("WARNING", msg)
def error(msg: str):    _emit("ERROR", msg)
def critical(msg: str): _emit("CRITICAL", msg)

# convenience alias
log = info
