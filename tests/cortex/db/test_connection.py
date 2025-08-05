from cortex.db.engine_factory import get_db_engine

def test():
    engine = get_db_engine()
    if engine.test_connection():
        print("✅ DB connection successful!")
    else:
        print("❌ DB connection failed.")

if __name__ == "__main__":
    test()
