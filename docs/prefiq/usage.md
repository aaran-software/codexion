# 📖 Prefiq CLI — Usage Guide

Prefiq provides a unified CLI for managing server, database, and utilities.

---

## 🔹 General

```
prefiq [GROUP] [COMMAND] [OPTIONS]
```

* **GROUP** → logical category (server, run, …)
* **COMMAND** → action inside that group
* **OPTIONS** → flags or arguments

---

## 🔹 Server

Start and bootstrap the Prefiq server.

```
prefiq server run [ENV]
```

**Examples:**

```
prefiq server run              # default = development
prefiq server run production   # run in production mode
```

---

## 🔹 Database / Migration

Run migrations, seeds, or reset the DB.

```
prefiq run migrate [OPTIONS]
```

**Options:**

* `--seed` → also run seeders after applying migrations
* `--fresh` → drop all tables before migrating
* `--steps N` → run only N pending migrations (if rollback/stepwise supported)

**Examples:**

```
prefiq run migrate             # apply all migrations
prefiq run migrate --seed      # migrate and seed
prefiq run migrate --fresh     # drop, migrate
prefiq run migrate --fresh --seed
```

---

## 🔹 Utilities

Tools for project sanity checks and housekeeping.

```
prefiq run sanity
prefiq run clear-cache [PATH]
```

**Examples:**

```
prefiq run sanity              # verify settings + DB connectivity
prefiq run clear-cache         # clear __pycache__ folders in current dir
prefiq run clear-cache ./apps  # clear only under ./apps
```

---

## 🔹 Version & Help

```
prefiq --help
prefiq --version
```

---

📌 **Typical workflow for a developer:**

1. Bootstrap DB fresh:

   ```
   prefiq run migrate --fresh --seed
   ```
2. Sanity check everything:

   ```
   prefiq run sanity
   ```
3. Start server in dev mode:

   ```
   prefiq server run dev
   ```