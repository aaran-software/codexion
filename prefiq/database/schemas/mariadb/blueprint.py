from typing import List, Optional, Tuple, Dict

# --- add this set at top-level ---
_SQL_KEYWORDS_NOQUOTE = {
    "CURRENT_TIMESTAMP",
    "CURRENT_TIMESTAMP()",
    "CURRENT_DATE",
    "CURRENT_DATE()",
    "CURRENT_TIME",
    "CURRENT_TIME()",
    "NOW()",
    "LOCALTIME",
    "LOCALTIMESTAMP",
}

class TableBlueprint:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns: List[str] = []
        self.foreign_keys: List[str] = []
        self.indexes: List[str] = []
        self.unique_constraints: List[str] = []
        self.check_constraints: List[str] = []
        self._pending_fks: List[Dict[str, Optional[str | Tuple[str, str]]]] = []

    def _column_definition(self, name: str, type_def: str, nullable=True, default=None, unique=False) -> str:
        col = f"`{name}` {type_def}"
        if not nullable:
            col += " NOT NULL"
        if default is not None:
            col += f" DEFAULT {self._format_default(default)}"
        if unique:
            col += " UNIQUE"
        return col

    # --- fixed: don't quote SQL time keywords ---
    def _format_default(self, default):
        if isinstance(default, str):
            up = default.upper()
            if up in _SQL_KEYWORDS_NOQUOTE:
                return up
            return f"'{default}'"
        if isinstance(default, bool):
            return '1' if default else '0'
        return str(default)

    def id(self, name: str = "id"):
        self.columns.append(f"`{name}` INT AUTO_INCREMENT PRIMARY KEY")

    def string(self, name: str, length: int = 255, **kwargs):
        self.columns.append(self._column_definition(name, f"VARCHAR({length})", **kwargs))

    def text(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "TEXT", **kwargs))

    def longtext(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "LONGTEXT", **kwargs))

    def tinytext(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "TINYTEXT", **kwargs))

    def blob(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "BLOB", **kwargs))

    def tiny_integer(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "TINYINT", **kwargs))

    def integer(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "INT", **kwargs))

    def biginteger(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "BIGINT", **kwargs))

    def boolean(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "BOOLEAN", **kwargs))

    def datetime(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "DATETIME", **kwargs))

    def date(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "DATE", **kwargs))

    def json(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "JSON", **kwargs))

    def uuid(self, name: str, **kwargs):
        self.columns.append(self._column_definition(name, "CHAR(36)", **kwargs))

    def enum(self, name: str, values: List[str], constraint_name: Optional[str] = None, **kwargs):
        enum_values = ", ".join(f"'{v}'" for v in values)
        self.columns.append(self._column_definition(name, f"ENUM({enum_values})", **kwargs))
        if constraint_name:
            self.check_constraints.append(f"CONSTRAINT {constraint_name} CHECK (`{name}` IN ({enum_values}))")

    def check(self, condition: str, name: Optional[str] = None):
        if name:
            self.check_constraints.append(f"CONSTRAINT `{name}` CHECK ({condition})")
        else:
            self.check_constraints.append(f"CHECK ({condition})")

    def index(self, name: str, column: str):
        self.indexes.append(f"INDEX `{name}` (`{column}`)")

    def unique(self, name: str, columns: List[str]):
        cols = ", ".join(f"`{c}`" for c in columns)
        self.unique_constraints.append(f"UNIQUE KEY `{name}` ({cols})")

    def foreign_id(self, name: str):
        """Start defining a foreign key (chain with references(), on_delete(), on_update())"""
        self.columns.append(f"`{name}` INT")
        self._pending_fks.append({
            "column": name,
            "references": None,
            "on_delete": None,
            "on_update": None
        })
        return self

    def references(self, ref_table: str, ref_column: str = "id"):
        if self._pending_fks:
            self._pending_fks[-1]["references"] = (ref_table, ref_column)
        return self

    def on_delete(self, action: str):
        if self._pending_fks:
            self._pending_fks[-1]["on_delete"] = action
        return self

    def on_update(self, action: str):
        if self._pending_fks:
            self._pending_fks[-1]["on_update"] = action
        return self

    def _finalize_foreign_keys(self):
        for fk in self._pending_fks:
            if fk["references"]:
                col = fk["column"]
                ref_table, ref_column = fk["references"]
                clause = f"FOREIGN KEY (`{col}`) REFERENCES `{ref_table}`(`{ref_column}`)"
                if fk["on_delete"]:
                    clause += f" ON DELETE {fk['on_delete']}"
                if fk["on_update"]:
                    clause += f" ON UPDATE {fk['on_update']}"
                self.foreign_keys.append(clause)
        self._pending_fks.clear()

    def timestamps(self):
        self.columns.append("`created_at` DATETIME DEFAULT CURRENT_TIMESTAMP")
        self.columns.append("`updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")

    def soft_deletes(self, column_name: str = "deleted_at"):
        self.columns.append(f"`{column_name}` DATETIME NULL")

    def build_columns(self) -> str:
        self._finalize_foreign_keys()
        all_defs = self.columns + self.foreign_keys + self.check_constraints + self.unique_constraints + self.indexes
        return ",\n  ".join(all_defs)
