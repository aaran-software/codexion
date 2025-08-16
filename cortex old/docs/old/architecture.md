structured your architecture to mirror Laravel’s philosophy while staying Pythonic.

* **`main.py`** – Application entry point. Starts the lifecycle and runs the app.
* **`lifecycle.py`** – Handles the app boot lifecycle (similar to Laravel's HTTP Kernel or Console Kernel).
* **`boot.py`** – Executes one-time boot logic for providers or app setup.
* **`services.py`** – Holds service provider classes, each with `register()` and `boot()` methods.
* **`config.py`** – Loads and organizes configuration (env vars, service config, etc.).
* **`container.py`** – Simple IoC container or service locator for dependency injection.
* **`endpoints.py`** – Registers routes (API or web endpoints).
* **`core/database/migrations.py`** – Manages migration logic and schema versioning using raw SQL.


| Pythonic Option                             | Notes                   |
| ------------------------------------------- | ----------------------- |
| `Service`, `Manager`, `Component`, `Module` | E.g., `DatabaseService` |
| `Lifecycle`, `Engine`, `Core`, `AppRunner`  | Up to you               |
| `boot.py`, `init.py`, `startup.py`          | Prefer `boot.py`        |
