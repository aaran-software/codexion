# cortex/

from pathlib import Path
from types import SimpleNamespace

def get_base_table_files(folder: str = "base") -> list[SimpleNamespace]:
    """
    Discover all base/system migration files from the base_tables folder.
    Returns a list of objects with `.module` and `.path`.

    Example return:
        [ SimpleNamespace(module="base", path=Path(".../000_migration_table.py")) ]
    """
    base_dir = Path(__file__).parent  # points to cortex/database/base_tables
    py_files = sorted(f for f in base_dir.glob("*.py") if f.name[0].isdigit())

    return [
        SimpleNamespace(
            module=folder,
            path=py_file
        )
        for py_file in py_files
    ]
