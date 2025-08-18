import asyncio
from prefiq.core.contracts.base_provider import Application
from prefiq.repositories.user_repo_async import UserRepoAsync
from prefiq.repositories.models import User

async def main():
    app = Application.get_app()
    db = app.resolve("db")

    repo = UserRepoAsync(db)
    await repo.migrate()

    uid = await repo.create(User(email="alice@example.com", name="Alice"))
    print("created user id:", uid)

    u = await repo.get_by_id(uid)
    print("fetched:", u)

    users = await repo.list_active(10)
    print("active:", users)

if __name__ == "__main__":
    # make sure bootstrap ran (via python -m prefiq.core.runtime.bootstrap before,
    # or import & call the bootstrap.main() if needed)
    asyncio.run(main())
