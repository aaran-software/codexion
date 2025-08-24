from __future__ import annotations

import logging
from prefiq.core.provider import Provider  # base class you mentioned

logger = logging.getLogger(__name__)


class DevmetaProvider(Provider):
    """
    Minimal provider for the 'devmeta' app.
    Only implements `register` and logs when called.
    """

    def register(self, app) -> None:
        logger.info("DevmetaProvider.register() called for app=%r", getattr(app, "name", app))
        # If you prefer a hard print instead of logging, uncomment:
        # print("DevmetaProvider registered")
