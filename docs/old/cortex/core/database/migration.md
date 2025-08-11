# Directory Structure:
# cortex/
# └── core/
#     └── database/
#         └── migrations/
#             ├── runner.py     # Migration discovery & execution logic
#             ├── tracker.py    # Tracks applied migrations in `migrations` table
#             ├── rollback.py   # Reverses latest batch of migrations
#             ├── fresh.py      # Drops all tables and reruns all migrations
#             ├── drop.py       # Drops individual or all migrations
#             └── files/        # Folder where migration scripts live


✅ Full implementation added for:

runner.py: Base runner with OOP-style migration registration and execution

tracker.py: MigrationTracker class with full methods

rollback.py: Rolls back the latest batch

fresh.py: Drops all tables and reruns migrations

drop.py: Drops a specific migration