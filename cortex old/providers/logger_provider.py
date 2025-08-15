# providers/logger_provider.py

from cortex.services import ServiceProvider
from cortex.container import container
import logging

class LoggerServiceProvider(ServiceProvider):
    def register(self):
        logger = logging.getLogger("Codexion")
        logger.setLevel(logging.INFO)
        container.instance("logger", logger)

    def boot(self):
        logger = container.resolve("logger")
        logger.info("Logger booted successfully!")
