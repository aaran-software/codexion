def is_healthy(engine) -> bool:
    try:
        return engine.test_connection()
    except Exception:
        return False