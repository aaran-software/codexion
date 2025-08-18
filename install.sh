#!/bin/bash
mkdir -p apps/devmeta/{cli,migrations,services,api/routers,models,sync}

# top-level files
touch apps/devmeta/README.md
touch apps/devmeta/__init__.py
touch apps/devmeta/provider.py

# CLI
touch apps/devmeta/cli/__init__.py
touch apps/devmeta/cli/devmeta.py

# migrations (placeholders)
cat > apps/devmeta/migrations/0001_todos.sql <<'SQL'
-- TODO: create table todos (id, title, status, priority, project, due_at, created_at, updated_at, completed_at)
SQL
cat > apps/devmeta/migrations/0002_indexes.sql <<'SQL'
-- TODO: create indexes on todos(status) and todos(due_at)
SQL

# services
touch apps/devmeta/services/__init__.py
touch apps/devmeta/services/todo.py

# API (placeholders for future)
touch apps/devmeta/api/__init__.py
touch apps/devmeta/api/server.py
touch apps/devmeta/api/routers/__init__.py
touch apps/devmeta/api/routers/todos.py
touch apps/devmeta/api/routers/notes.py
touch apps/devmeta/api/routers/logs.py
touch apps/devmeta/api/routers/projects.py
touch apps/devmeta/api/routers/roadmap.py
touch apps/devmeta/api/routers/reviews.py

# models / sync (placeholders)
touch apps/devmeta/models/__init__.py
touch apps/devmeta/models/dto.py
touch apps/devmeta/sync/__init__.py
touch apps/devmeta/sync/ndjson.py

echo "✅ devmeta skeleton created under apps/devmeta/"