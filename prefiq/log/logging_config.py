# prefiq/log/logging_config.py

import logging
import re
from logging.config import dictConfig

class DropBookkeepingSQL(logging.Filter):
    """Hide the framework's migrations table checks (defensive variations)."""
    _pat = re.compile(
        r"create\s+table\s+if\s+not\s+exists\s+`?migrations`?",
        re.IGNORECASE
    )
    def filter(self, record: logging.LogRecord) -> bool:
        # Check formatted message
        msg = record.getMessage() or ""
        if self._pat.search(msg):
            return False
        # Check common extra fields where SQL might be stored
        for attr in ("query", "sql", "statement"):
            val = getattr(record, attr, None)
            if isinstance(val, str) and self._pat.search(val):
                return False
        return True

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,

    "filters": {
        "drop_migrations_bootstrap": {
            "()": DropBookkeepingSQL
        }
    },

    "formatters": {
        # Use your TextFormatter (with colors and base namespace trimming)
        "colored": {
            "()": "prefiq.log.logger.TextFormatter",
            "base_ns": "prefiq",
            "use_color": True
        },
        # Simple plain fallback if needed
        "plain": {
            "format": "%(asctime)s [%(levelname)s] %(name)s | %(message)s"
        }
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "colored"
        },
        "console_filtered": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "colored",
            "filters": ["drop_migrations_bootstrap"]
        }
    },

    "loggers": {
        # Keep migration code verbose (both short and namespaced)
        "migrate":            {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "prefiq.migrate":     {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "app.migrations":     {"level": "DEBUG", "handlers": ["console"], "propagate": False},
        "prefiq.app.migrations": {"level": "DEBUG", "handlers": ["console"], "propagate": False},

        # Quiet framework-y channels to INFO
        "bootstrap":          {"level": "INFO", "handlers": ["console"], "propagate": False},
        "prefiq.bootstrap":   {"level": "INFO", "handlers": ["console"], "propagate": False},
        "settings":           {"level": "INFO", "handlers": ["console"], "propagate": False},
        "prefiq.settings":    {"level": "INFO", "handlers": ["console"], "propagate": False},
        "db.provider":        {"level": "INFO", "handlers": ["console"], "propagate": False},
        "prefiq.db.provider": {"level": "INFO", "handlers": ["console"], "propagate": False},

        # Show SQL at INFO but drop the migrations-table boilerplate
        "db.query":           {"level": "INFO", "handlers": ["console_filtered"], "propagate": False},
        "prefiq.db.query":    {"level": "INFO", "handlers": ["console_filtered"], "propagate": False},
    },

    # Correct root config (use "root", not empty-string)
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
})
