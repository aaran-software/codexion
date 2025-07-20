# cortex/database/seeders/user_seeder.py

from cortex.models.user import User, Base
from cortex.DTO.database import engine, DAL
from datetime import datetime
from sqlalchemy import select

def seed_user():
    Base.metadata.create_all(bind=engine)

    with DAL() as session:
        exists = session.scalar(select(User).where(User.username == "admin"))
        if exists:
            print("Admin user already exists.")
            return

        user = User(
            username="admin",
            password="admin123",  # You can hash this later
            created_at=datetime.utcnow()
        )
        session.add(user)
        session.commit()
        print("Admin user seeded successfully.")

if __name__ == "__main__":
    seed_user()
