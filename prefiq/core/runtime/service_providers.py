from __future__ import annotations
from typing import List, Type

from prefiq.core.provider import Provider
from prefiq.core.runtime.discover_provider import discover_providers


def get_service_providers() -> List[Type[Provider]]:
    """
    Public hook consumed by your bootstrap.
    Returns discovered & ordered Provider classes.
    """
    return discover_providers()
