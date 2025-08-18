# prefiq/database/dialects/mongodb.py
from .base import Dialect

class MongoDBDialect(Dialect):
    name = "mongodb"

    def quote_ident(self, ident: str) -> str:
        # no quoting needed for collection names
        return ident

    def create_table_suffix(self) -> str:
        return ""

    def normalize_params(self, sql, params):
        return sql, params
