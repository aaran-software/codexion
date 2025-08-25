# prefiq/database/schemas/sqlite/blueprint.py
from __future__ import annotations
from typing import List, Optional, Tuple, Dict

_SQL_KEYWORDS_NOQUOTE = {
    "CURRENT_TIMESTAMP", "CURRENT_DATE", "CURRENT_TIME",
    "LOCALTIME", "LOCALTIMESTAMP",
}

def q(name: str) -> str:
    return f"\"{name}\""

class TableBlueprint:
    """
    SQLite flavor: double quotes, INTEGER PRIMARY KEY AUTOINCREMENT, no inline indexes.
    """
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns: List[str] = []
        self.foreign_keys: List[str] = []
        self.unique_constraints: List[str] = []
        self.check_constraints: List[str] = []
        # (index_name, [cols...])
        self._index_meta: List[Tuple[str, List[str]]] = []
        self._pending_fks: List[Dict[str, Optional[str | Tuple[str, str]]]] = []

    def _column_definition(self, name: str, type_def: str, nullable=True, default=None, unique=False) -> str:
        col = f"{q(name)} {type_def}"
        if not nullable:
            col += " NOT NULL"
        if default is not None:
            col += f" DEFAULT {self._format_default(default)}"
        if unique:
            col += " UNIQUE"
        return col

    def _format_default(self, default):
        if isinstance(default, str):
            up = default.upper()
            if up in _SQL_KEYWORDS_NOQUOTE:
                return up
            return f"'{default}'"
        if isinstance(default, bool):
            return '1' if default else '0'
        return str(default)

    # columns
    def id(self, name: str = "id"):
        self.columns.append(f"{q(name)} INTEGER PRIMARY KEY AUTOINCREMENT")

    def string(self, name: str, length: int = 255, **kwargs): self.columns.append(self._column_definition(name, f"TEXT", **kwargs))
    def text(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def longtext(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def tinytext(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def blob(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "BLOB", **kwargs))
    def tiny_integer(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "INTEGER", **kwargs))
    def integer(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "INTEGER", **kwargs))
    def biginteger(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "INTEGER", **kwargs))
    def boolean(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "INTEGER", **kwargs))
    def datetime(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def date(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def json(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def uuid(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))

    def enum(self, name: str, values: List[str], constraint_name: Optional[str] = None, **kwargs):
        self.columns.append(self._column_definition(name, "TEXT", **kwargs))
        enum_values = ", ".join(f"'{v}'" for v in values)
        cname = q(constraint_name) if constraint_name else ""
        self.check_constraints.append(f"{'CONSTRAINT ' + cname + ' ' if cname else ''}CHECK ({q(name)} IN ({enum_values}))")

    def check(self, condition: str, name: Optional[str] = None):
        if name: self.check_constraints.append(f"CONSTRAINT {q(name)} CHECK ({condition})")
        else: self.check_constraints.append(f"CHECK ({condition})")

    # ── FIX: accept index(column|[columns], name=None) and auto-name when needed ──
    def index(self, column: str | List[str], name: Optional[str] = None):
        cols = [c.strip() for c in (column if isinstance(column, list) else [column])]
        idx_name = name or f"{self.table_name}_{'_'.join(cols)}_idx"
        self._index_meta.append((idx_name, cols))

    def unique(self, name: str, columns: List[str]):
        cols = ", ".join(q(c) for c in columns)
        self.unique_constraints.append(f"CONSTRAINT {q(name)} UNIQUE ({cols})")

    # Fluent FK helpers (optional)
    def foreign_id(self, name: str):
        self.columns.append(f"{q(name)} INTEGER")
        self._pending_fks.append({"column": name, "references": None, "on_delete": None, "on_update": None})
        return self

    def references(self, ref_table: str, ref_column: str = "id"):
        if self._pending_fks: self._pending_fks[-1]["references"] = (ref_table, ref_column)
        return self

    def on_delete(self, action: str):
        if self._pending_fks: self._pending_fks[-1]["on_delete"] = action
        return self

    def on_update(self, action: str):
        if self._pending_fks: self._pending_fks[-1]["on_update"] = action
        return self

    def _finalize_foreign_keys(self):
        for fk in self._pending_fks:
            if fk["references"]:
                col = fk["column"]; ref_table, ref_column = fk["references"]
                clause = f"FOREIGN KEY ({q(col)}) REFERENCES {q(ref_table)}({q(ref_column)})"
                if fk["on_delete"]: clause += f" ON DELETE {fk['on_delete']}"
                if fk["on_update"]: clause += f" ON UPDATE {fk['on_update']}"
                self.foreign_keys.append(clause)
        self._pending_fks.clear()

    def timestamps(self):
        self.columns.append(f"{q('created_at')} TEXT DEFAULT CURRENT_TIMESTAMP")
        self.columns.append(f"{q('updated_at')} TEXT DEFAULT CURRENT_TIMESTAMP")

    def soft_deletes(self, column_name: str = "deleted_at"):
        self.columns.append(f"{q(column_name)} TEXT NULL")

    def build_columns(self) -> str:
        self._finalize_foreign_keys()
        all_defs = self.columns + self.foreign_keys + self.check_constraints + self.unique_constraints
        return ",\n  ".join(all_defs)

    @property
    def index_meta(self) -> List[Tuple[str, List[str]]]:
        return list(self._index_meta)
