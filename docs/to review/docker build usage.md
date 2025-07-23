Here's a **help file with clear usage instructions** 

---

# 🐳 Prefiq Docker CLI Help

**Command Group:** `prefiq docker`
**Description:** Docker utility commands to scaffold Dockerfiles, compose files, and proxy configs (Traefik, Nginx, DB).

---

## 🔧 Commands

### 1. `build`

Generate a Dockerfile for your application.

```bash
prefiq docker build --name <name>
```

**Options:**

* `--name`, `-n`: Name for Dockerfile (e.g., `app`). If not provided, will prompt.

📌 **Example:**

```bash
prefiq docker build --name myapp
```

---

### 2. `compose`

Generate a `docker-compose.yml` for an app with domain and port.

```bash
prefiq docker compose
```

**Prompts:**

* `Domain`: e.g., `soft.com`
* `Port`: e.g., `8000`

📌 **Example:**

```bash
prefiq docker compose
# Will ask:
# Domain (e.g., sundar.com): soft.com
# Port (e.g., 8000): 8080
```

---

### 3. `mariadb`

Generate a MariaDB `docker-compose-mariadb.yml`.

```bash
prefiq docker mariadb
```

**Prompts:**

* `MariaDB database name` (default: `mariadb`)
* `MariaDB root password` (default: `DbPass1@@`)

📌 **Example:**

```bash
prefiq docker mariadb
```

---

### 4. `pgdb`

Generate a PostgreSQL `docker-compose-postgres.yml`.

```bash
prefiq docker pgdb
```

**Prompts:**

* `Postgres database name` (default: `postgres`)
* `Postgres root password` (default: `PgPass1@@`)

📌 **Example:**

```bash
prefiq docker pgdb
```

---

### 5. `nginx`

Generate an Nginx reverse proxy `docker-compose-nginx.yml`.

```bash
prefiq docker nginx
```

**Prompts:**

* `App service name`: e.g., `cloud`
* `Internal port`: e.g., `8000`

📌 **Example:**

```bash
prefiq docker nginx
```

---

### 6. `traefik`

Generate a Traefik proxy config `docker-compose-traefik.yml`.

```bash
prefiq docker traefik
```

**Prompts:**

* `Email`: used for SSL via Let's Encrypt

📌 **Example:**

```bash
prefiq docker traefik
```

---

## ℹ️ Notes

* All output files will be placed under the `docker/` directory in your project.
* Ensure you have write permissions for that folder.
* Default values are used when possible, but you can override them via prompt.

---

Let me know if you'd like to include this as an actual `--help` command or generate it dynamically.
