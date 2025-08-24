from prefiq.settings.get_settings import load_settings
from prefiq.log.logger import configure_logging, get_logger

def init_logger(name: str = "prefiq.bootstrap"):
    s = load_settings()
    configure_logging(
        level=getattr(s, "LOG_LEVEL", "INFO"),
        fmt=getattr(s, "LOG_FORMAT", "json"),
        base_logger=getattr(s, "LOG_NAMESPACE", "prefiq"),
        color=getattr(s, "LOG_COLOR", None),
    )
    return get_logger(name)
