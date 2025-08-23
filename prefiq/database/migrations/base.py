# prefiq/database/migrations/base.py

class Migrations:
    APP_NAME: str = "cortex"
    TABLE_NAME: str = "base"
    ORDER_INDEX: int = 0

    @classmethod
    def up(cls) -> None:
        raise NotImplementedError

    @classmethod
    def down(cls) -> None:
        pass
