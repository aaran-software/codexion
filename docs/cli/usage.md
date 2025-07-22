Here's a `USAGE.md` file tailored for your **Prefiq App CLI** focusing on app configuration management (installing, updating, listing, and deleting apps), assuming you're using `Typer` and a structure like `prefiq app ...`:

---

# 🧰 Prefiq CLI – App Management Usage Guide

Manage your app configurations easily using the `prefiq` CLI.

---

## 📦 Installing a New App

```bash
prefiq app install <app-name> --version <version>
```

✅ **Example:**

```bash
prefiq app install billing --version 1.0.0
```

Installs the app and adds it to `app.cfg` with the specified version.

---

## 🔁 Updating an App

```bash
prefiq app update <app-name> <version>
```

📌 Or to set the latest version:

```bash
prefiq app update <app-name> --latest
```

✅ **Examples:**

```bash
prefiq app update crm 2.1.0
prefiq app update crm --latest
```

If neither a version nor `--latest` is provided, an error will be shown.

---

## 📜 Listing All Apps

```bash
prefiq app list
```

Displays all apps listed in `app.cfg` with their version numbers.

---

## ❌ Deleting an App

```bash
prefiq app delete <app-name>
```

✅ **Example:**

```bash
prefiq app delete billing
```

Removes the specified app section from `app.cfg`.

---

## 🛠️ Generating Default Config Files

Automatically creates `app.cfg`, `api.cfg`, and `docker.cfg` with default content (if missing):

```bash
prefiq config init
```

This uses defaults like:

```ini
# app.cfg
[cxsun]
version = 1.2.0

[crm]
version = 0.9.5
```

---

## 📂 Config Path

Config files are stored at:

```
~/.prefiq/
```

This includes:

* `app.cfg`
* `api.cfg`
* `docker.cfg`

Use `CPATH.CONFIG_DIR` in code to access this directory.

---

## ✅ Notes

* All commands will create the config directory and files if they don't already exist.
* Use the CLI as `prefiq app <command> [options]`.

---

Let me know if you'd like to include screenshots, diagrams, or link this doc from the CLI help screen (`--help`).
