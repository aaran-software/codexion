import os, glob, importlib.util
from prefiq.log.logger import get_logger
from prefiq.database.schemas.queries import record_migration_applied

LOG = get_logger("devmeta.migrator")

class DevMetaMigrator:
    def __init__(self, dir, conn):
        self.dir = dir
        self.conn = conn

    def _load_py_migration(self, path):
        spec = importlib.util.spec_from_file_location("mig", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore
        return mod

    def migrate(self, done: list[str], MIGR_TABLE: str = "migrations"):
        applied = 0

        # --- 1. run *.sql migrations -------------------------------
        for idx, path in enumerate(sorted(glob.glob(os.path.join(self.dir, "m*.sql"))), start=1):
            name = os.path.basename(path)
            if name in done:
                continue
            LOG.info("apply_migration", extra={"file": name, "index": idx})
            with open(path, "r") as f:
                sql = f.read()
                self.conn.executescript(sql)
            record_migration_applied(self.conn, name, idx, "sql", MIGR_TABLE)
            applied += 1

        # --- 2. run *.py migrations (builder DSL) ------------------
        for idx, path in enumerate(sorted(glob.glob(os.path.join(self.dir, "m*.py"))), start=1):
            name = os.path.basename(path)
            if name in done:
                continue
            LOG.info("apply_migration", extra={"file": name, "index": idx})
            mod = self._load_py_migration(path)
            if not hasattr(mod, "up"):
                raise AttributeError(f"{name} has no up() function")
            mod.up()  # call the DSL migration
            record_migration_applied(self.conn, name, idx, "builder-dsl", MIGR_TABLE)
            applied += 1

        return applied
