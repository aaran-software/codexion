# =============================================================
# Health Check Utility (health.py)
#
# Author: ChatGPT
# Created: 2025-08-06
#
# Purpose:
#   - Provide a universal health check function for any DB engine.
#
# Notes for Developers:
#   - Engine must implement `test_connection()` method.
#   - Returns `True` if connection succeeds, `False` otherwise.
# =============================================================

def is_healthy(engine) -> bool:
    """
    Check if a given engine is alive and responsive.

    :param engine: A database engine instance with `test_connection()` method
    :return: True if healthy, False if any error is raised
    """
    try:
        return engine.test_connection()
    except Exception:
        return False
