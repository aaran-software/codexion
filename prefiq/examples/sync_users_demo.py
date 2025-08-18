from prefiq.core.contracts.base_provider import Application
from prefiq.repositories.user_repo_sync import UserRepoSync
from prefiq.repositories.models import User

def main():
    app = Application.get_app()
    db = app.resolve("db")  # ensure DB_MODE=sync in settings for this demo

    repo = UserRepoSync(db)
    repo.migrate()

    uid = repo.create(User(email="bob@example.com", name="Bob"))
    print("created user id:", uid)

    u = repo.get_by_id(uid)
    print("fetched:", u)

    print("active:", repo.list_active(10))

if __name__ == "__main__":
    main()
