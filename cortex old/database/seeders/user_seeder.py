# cortex/database/seeders/user_seeder.py

from pathlib import Path
import sys

# ✅ Correct path: go up THREE levels to reach project root
project_root = Path(__file__).resolve().parents[3]
print(f"Adding project root to sys.path: {project_root}")
sys.path.insert(0, str(project_root))  # ensures cortex is importable


from cortex.models.user import User, Base
from cortex.DTO.dal import engine, SessionLocal
from sqlalchemy import select
from datetime import datetime, timezone
from cortex.core.hashing import hash_password

def seed_user():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as session:
        exists = session.scalar(select(User).where(User.username == "admin"))
        if exists:
            print("Admin user already exists.")
            return

        user = User(
            username="admin",
            password=hash_password("admin123"),
            created_at=datetime.now(timezone.utc)
        )
        session.add(user)
        session.commit()
        print("Admin user seeded successfully.")

if __name__ == "__main__":
    seed_user()
