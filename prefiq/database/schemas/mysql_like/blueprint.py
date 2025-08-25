# prefiq/database/schemas/mysql_like/blueprint.py
from __future__ import annotations
from typing import List, Optional, Tuple, Dict, Iterable

_SQL_KEYWORDS_NOQUOTE = {
    "CURRENT_TIMESTAMP", "CURRENT_TIMESTAMP()", "CURRENT_DATE", "CURRENT_DATE()",
    "CURRENT_TIME", "CURRENT_TIME()", "NOW()", "LOCALTIME", "LOCALTIMESTAMP",
}

def q(name: str) -> str:
    return f"`{name}`"


class TableBlueprint:
    """
    MySQL/MariaDB flavor: backticks, ENUM, AUTO_INCREMENT, inline indexes allowed.
    Also records index metadata for external creation if needed.
    """
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns: List[str] = []
        self.foreign_keys: List[str] = []
        self.indexes_inline: List[str] = []                  # goes into CREATE TABLE
        self._index_meta: List[Tuple[str, List[str]]] = []   # optional: for builders creating after
        self.unique_constraints: List[str] = []
        self.check_constraints: List[str] = []
        self._pending_fks: List[Dict[str, Optional[str | Tuple[str, str]]]] = []

    # ---------------- internal helpers ----------------
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

    # ---------------- column helpers ----------------
    def id(self, name: str = "id"):
        self.columns.append(f"{q(name)} INT AUTO_INCREMENT PRIMARY KEY")

    def string(self, name: str, length: int = 255, **kwargs):
        self.columns.append(self._column_definition(name, f"VARCHAR({length})", **kwargs))

    def text(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TEXT", **kwargs))
    def longtext(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "LONGTEXT", **kwargs))
    def tinytext(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TINYTEXT", **kwargs))
    def blob(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "BLOB", **kwargs))
    def tiny_integer(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "TINYINT", **kwargs))
    def integer(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "INT", **kwargs))
    def biginteger(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "BIGINT", **kwargs))
    def boolean(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "BOOLEAN", **kwargs))
    def datetime(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "DATETIME", **kwargs))
    def date(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "DATE", **kwargs))
    def json(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "JSON", **kwargs))
    def uuid(self, name: str, **kwargs): self.columns.append(self._column_definition(name, "CHAR(36)", **kwargs))

    def enum(self, name: str, values: List[str], constraint_name: Optional[str] = None, **kwargs):
        enum_values = ", ".join(f"'{v}'" for v in values)
        self.columns.append(self._column_definition(name, f"ENUM({enum_values})", **kwargs))
        # optional CHECK to mirror portability if desired
        if constraint_name:
            self.check_constraints.append(f"CONSTRAINT {q(constraint_name)} CHECK ({q(name)} IN ({enum_values}))")

    def check(self, condition: str, name: Optional[str] = None):
        if name:
            self.check_constraints.append(f"CONSTRAINT {q(name)} CHECK ({condition})")
        else:
            self.check_constraints.append(f"CHECK ({condition})")

    # ---------------- index helpers (flexible) ----------------
    # Accept:
    #   index("status")
    #   index(["project_id","status"])
    #   index("idx_tasks_project", "project_id")
    #   index("idx_tasks_proj_status", ["project_id","status"])
    def index(self, *args, **kwargs):
        if not args and not kwargs:
            raise TypeError("index() requires at least 1 argument")

        # Parse arguments
        name: Optional[str] = kwargs.get("name")
        columns = kwargs.get("column") or kwargs.get("columns")

        if columns is None:
            if len(args) == 1:            # columns only
                columns = args[0]
            elif len(args) == 2:          # name, columns
                name, columns = args
            else:
                raise TypeError("index() accepts (columns) or (name, columns)")

        # Normalize columns list
        if isinstance(columns, str):
            cols = [columns.strip()]
        elif isinstance(columns, Iterable):
            cols = [str(c).strip() for c in columns if str(c).strip()]
        else:
            raise TypeError("columns must be a string or an iterable of strings")

        if not cols:
            raise ValueError("index() requires at least one column")

        # Auto-generate a name if not provided
        idx_name = name or f"idx_{self.table_name}_" + "_".join(cols)

        # Record both inline and meta (so builders may choose either route)
        cols_join = ", ".join(q(c) for c in cols)
        self.indexes_inline.append(f"INDEX {q(idx_name)} ({cols_join})")
        self._index_meta.append((idx_name, cols))

    def unique(self, name: str, columns: List[str]):
        cols = ", ".join(q(c) for c in columns)
        self.unique_constraints.append(f"UNIQUE KEY {q(name)} ({cols})")

    # ---------------- FK fluent API ----------------
    def foreign_id(self, name: str):
        self.columns.append(f"{q(name)} INT")
        self._pending_fks.append({"column": name, "references": None, "on_delete": None, "on_update": None})
        return self

    def references(self, ref_table: str, ref_column: str = "id"):
        if self._pending_fks:
            self._pending_fks[-1]["references"] = (ref_table, ref_column)
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

    # ---------------- convenience columns ----------------
    def timestamps(self):
        self.columns.append(f"{q('created_at')} DATETIME DEFAULT CURRENT_TIMESTAMP")
        self.columns.append(f"{q('updated_at')} DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    def soft_deletes(self, column_name: str = "deleted_at"):
        self.columns.append(f"{q(column_name)} DATETIME NULL")

    # ---------------- SQL builders ----------------
    def build_columns(self) -> str:
        self._finalize_foreign_keys()
        # Inline indexes appended to CREATE TABLE for MySQL/MariaDB
        all_defs = self.columns + self.foreign_keys + self.check_constraints + self.unique_constraints + self.indexes_inline
        return ",\n  ".join(all_defs)

    # Optional: for builders that prefer post-create index statements
    @property
    def index_meta(self) -> List[Tuple[str, List[str]]]:
        return list(self._index_meta)
