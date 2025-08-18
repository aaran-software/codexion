from __future__ import annotations
from prefiq.core.contracts.base_provider import Application
from prefiq.repositories.user_repo_async import UserRepoAsync
from prefiq.repositories.user_repo_sync import UserRepoSync
from prefiq.repositories.audit_repo_async import AuditRepoAsync
from prefiq.repositories.audit_repo_sync import AuditRepoSync

# Async migration
async def up_async():
    app = Application.get_app()
    db = app.resolve("db")
    await UserRepoAsync(db).migrate()
    await AuditRepoAsync(db).migrate()

# Sync migration
def up_sync():
    app = Application.get_app()
    db = app.resolve("db")
    UserRepoSync(db).migrate()
    AuditRepoSync(db).migrate()
