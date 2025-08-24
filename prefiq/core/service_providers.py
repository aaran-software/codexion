from __future__ import annotations
from typing import List, Type
from prefiq.core.provider import Provider
from prefiq.core.discovery import discover_providers


def get_service_providers() -> List[Type[Provider]]:
    return discover_providers()
