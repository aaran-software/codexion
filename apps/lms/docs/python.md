# Python Roadmap: Beginner → Advanced (Phased & Numbered)

> A comprehensive, opinionated path from absolute beginner to professional-level Python. Follow the phases in order; pick one specialization track (or more) after Phase 8.

---

## Phase 0 — Environment & Habits (Foundation)

**Goal:** Set up a clean workflow so you can learn fast and avoid bad habits.

1. **Installations**
   1.1 Install CPython (latest LTS-ish release).
   1.2 Install an editor: VS Code / PyCharm.
   1.3 Configure PATH, terminals (PowerShell/Bash), and shell basics.
2. **Virtual Envs & Packages**
   2.1 `python -m venv`, activate/deactivate.
   2.2 `pip`/`pipx` usage; upgrade pip safely.
   2.3 Requirements files vs `pyproject.toml` (preview).
3. **Git & Project Hygiene**
   3.1 Git basics (init, add, commit, branch, merge).
   3.2 GitHub/GitLab remote workflow (pull request basics).
   3.3 `.gitignore`, `README.md`, `LICENSE`, the `src/` layout.
4. **Reading Docs & PEPs**
   4.1 Navigating the Python docs.
   4.2 PEP 8 (style), PEP 20 (Zen), how to skim PEPs.
5. **Mindset & Study Loop**
   5.1 Spaced repetition for syntax & stdlib names.
   5.2 Build-first learning: small project each week.
   5.3 Keep a "bugs & lessons" diary.

**Milestone M0:** You can create a venv, install a package, run a script, push to GitHub.

---

## Phase 1 — Core Python Fundamentals (Beginner)

**Goal:** Be fluent with the language basics and control flow.

1. **Syntax & Types**
   1.1 Expressions, statements, REPL.
   1.2 Numbers (`int`, `float`, `Decimal`), booleans, `None`.
   1.3 Strings: slicing, methods, f-strings.
2. **Collections & Iteration**
   2.1 Lists, tuples, sets, dicts.
   2.2 Comprehensions (list/set/dict).
   2.3 Iteration with `for`/`while`, `range()`.
3. **Control Flow & Errors**
   3.1 `if/elif/else`, truthiness.
   3.2 Exceptions: `try/except/else/finally`, `raise`.
4. **Functions**
   4.1 Defining, returning, docstrings.
   4.2 Parameters: default, `*args`, `**kwargs`, keyword-only, positional-only.
   4.3 Scope, closures.
5. **Modules & Packages**
   5.1 `import` mechanics, `__name__ == "__main__"`.
   5.2 Creating your own modules.
6. **I/O**
   6.1 Input/print, basic file read/write, newline encodings.
7. **Style & Linting (light)**
   7.1 PEP 8, formatter (Black) preview.

**Practice P1:**

* Calculator, number guessing, text-based menu app, unit converter.
* Small script that reads/writes CSV.

**Milestone M1:** Implement a CLI script with functions, error handling, and a clean module structure.

---

## Phase 2 — Standard Library Power (Early-Intermediate)

**Goal:** Work effectively with the most useful stdlib modules.

1. **Files & Paths** — `pathlib`, `os`, `shutil`
2. **Dates/Times** — `datetime`, `zoneinfo`, `time`
3. **Data Formats** — `json`, `csv`, `configparser`, `tomllib`
4. **Math & Stats** — `math`, `statistics`, `random`, `secrets`
5. **Collections Toolbox** — `collections` (Counter, deque, defaultdict, namedtuple), `dataclasses`
6. **Functional Helpers** — `itertools`, `functools`, `operator`
7. **Logging** — structured logs, levels, handlers
8. **CLI Building** — `argparse` (and preview Typer/Click)
9. **Packaging Basics** — venv recap, editable installs, `pip-tools`/Poetry concept

**Practice P2:**

* Log-structured file organizer.
* Config-driven data converter (CSV ⇄ JSON ⇄ TOML).

**Milestone M2:** A robust CLI with config files, logs, and tests for happy/error paths.

---

## Phase 3 — OOP & Python Data Model (Intermediate)

**Goal:** Design maintainable Pythonic APIs.

1. **Classes & Instances** — attributes, methods, `__init__`
2. **Dunder Methods** — `__repr__`, `__str__`, ordering, hashing, equality
3. **Inheritance vs Composition** — mixins, interfaces, delegation
4. **Abstract Base Classes** — `abc.ABC`, `@abstractmethod`
5. **Properties & Descriptors** — computed attributes, validation
6. **Protocols & Duck Typing** — `typing.Protocol`
7. **Dataclasses & Attrs** — defaults, post-init, frozen models
8. **Design Patterns** — Strategy, Factory, Adapter, Observer (pythonic takes)

**Practice P3:**

* Small domain model (library/store/inventory) with dataclasses & protocols.
* `Repository` pattern over a file/DB backend.

**Milestone M3:** Ship a reusable package exposing a clean object model and type hints.

---

## Phase 4 — Testing, Types & Code Quality (Professional Basics)

**Goal:** Prevent regressions, communicate intent, and enforce quality.

1. **Unit Testing** — `pytest`, structuring tests, parametrization, fixtures
2. **Coverage & CI** — coverage reports, GitHub Actions basics
3. **Type Hints** — PEP 484/563/695 concepts, `typing` (Union, Optional, Literal, TypedDict, NewType, Generic)
4. **Type Checking** — mypy/pyright, strictness levels
5. **Static Analysis** — ruff/flake8, isort, Black
6. **Docs** — docstrings, Sphinx/MkDocs, MkDocs Material
7. **Property-Based Testing** — `hypothesis`

**Practice P4:**

* Convert an existing project to strict typing; add CI, coverage, and docs.

**Milestone M4:** PR checks enforce formatting, linting, typing, and tests.

---

## Phase 5 — Iterators, Generators, Decorators & Context Managers (Advanced Language)

**Goal:** Master Python’s control constructs and extensibility.

1. **Iteration Protocol** — `__iter__`, `__next__`, custom iterables
2. **Generators** — `yield`, pipelines, `send/throw/close`, backpressure basics
3. **Comprehensions** — lazy vs eager patterns, pitfalls
4. **Decorators** — function/class decorators, `functools.wraps`, memoization (`lru_cache`)
5. **Context Managers** — `with`, `contextlib` (`closing`, `suppress`, `ExitStack`)
6. **Pattern Matching** — `match/case` semantics & when to use

**Practice P5:**

* Build a streaming CSV processor with generator pipelines and context managers.
* Implement a timing/caching decorator suite.

**Milestone M5:** You can extend behavior cleanly without subclassing using decorators/contexts.

---

## Phase 6 — Concurrency, Parallelism & Async IO (Advanced)

**Goal:** Choose the right model for CPU vs IO work and implement it safely.

1. **GIL & Work Types** — CPU-bound vs IO-bound; choose model
2. **Threads** — `threading`, Locks, Queues, Futures patterns
3. **Processes** — `multiprocessing`, `concurrent.futures.ProcessPoolExecutor`
4. **AsyncIO** — event loop, coroutines, tasks, cancellation, `async`/`await`
5. **Async Networking** — `aiohttp`, websockets, backpressure
6. **Performance & Safety** — deadlocks, race conditions, timeouts, retries
7. **Profiling** — `cProfile`, `timeit`, `tracemalloc`

**Practice P6:**

* Multi-downloader: compare threads vs asyncio.
* Parallel image resizer (process pool).

**Milestone M6:** A benchmarked program selecting the correct concurrency model with clear wins.

---

## Phase 7 — Data Persistence & Messaging

**Goal:** Move beyond files to robust state and communication.

1. **Relational DBs** — SQLite (`sqlite3`), PostgreSQL basics
2. **ORMs** — SQLAlchemy Core/ORM, sessions, transactions, migrations (Alembic)
3. **NoSQL (overview)** — Redis (caching), MongoDB (document)
4. **Validation** — Pydantic v2 models & settings
5. **Caching** — `functools.lru_cache`, Redis, cache invalidation concepts
6. **Message Brokers** — RabbitMQ/Kafka (producer/consumer fundamentals)

**Practice P7:**

* Build a task tracker with SQLAlchemy and Alembic migrations; add Redis cache.

**Milestone M7:** Data model with migrations and a repeatable local dev DB workflow.

---

## Phase 8 — HTTP, APIs & Integration

**Goal:** Consume and produce reliable APIs.

1. **HTTP Fundamentals** — methods, status codes, idempotency
2. **Clients** — `requests`/`httpx` (sync/async), retries, exponential backoff
3. **Auth** — API keys, OAuth2 (client credentials, auth code), JWT
4. **Build APIs** — FastAPI (routing, deps, validation, OpenAPI)
5. **Docs & Testing** — schema, contracts, contract tests
6. **Resilience** — timeouts, circuit breakers, rate limiting

**Practice P8:**

* Public-API client library with retries and typed models.
* FastAPI microservice with OpenAPI and tests.

**Milestone M8:** Ship an API that’s typed, validated, documented, and tested.

---

# Specialization Tracks (pick 1–3 after Phase 8)

## Track A — Web Development (Flask/FastAPI/Django)

1. **Templating & Forms** — Jinja, WTForms
2. **Auth & Sessions** — cookies vs JWT, CSRF, CORS
3. **Django Deep Dive** — models, admin, ORM queries, signals
4. **Async Web** — ASGI, uvicorn/gunicorn, background tasks
5. **Caching & Jobs** — Redis, Celery/RQ, periodic tasks
6. **File Handling** — uploads, static/media, CDN
7. **Security** — XSS, SQLi, SSRF prevention

**Capstone WA:** Production-ready service (auth, admin, caching, background jobs, metrics).

---

## Track B — Data Science & ML

1. **Numerics** — NumPy (vectorization, broadcasting)
2. **DataFrames** — pandas (joins, groupby, time series)
3. **Viz** — Matplotlib/Seaborn; plotting best practices
4. **ML** — scikit-learn pipelines, cross-val, metrics
5. **Deep Learning (overview)** — PyTorch/TensorFlow, training loops
6. **MLOps (intro)** — experiment tracking, model packaging, batch vs online

**Capstone DS:** End-to-end project: clean → explore → model → evaluate → deploy (batch API).

---

## Track C — Automation & Scraping

1. **Scraping** — `requests` + `BeautifulSoup`, Scrapy for large crawls
2. **Browser Automation** — Playwright/Selenium
3. **Docs/Spreadsheets** — `openpyxl`, `python-docx`, `pdfminer`/`PyPDF`
4. **Task Scheduling** — APScheduler, cron concepts
5. **Desktop Ops** — `pyautogui` (carefully, with failsafes)

**Capstone AU:** Personal data pipeline (scrape → clean → store → report, scheduled weekly).

---

## Track D — DevOps, Packaging & Deployment

1. **Packaging** — `pyproject.toml`, build backends (setuptools/hatch/poetry), wheels vs sdists
2. **Versioning** — SemVer, changelogs, conventional commits
3. **Docker** — multi-stage builds, slim images, `.dockerignore`
4. **12-Factor Apps** — config via env vars, logs to stdout
5. **CI/CD** — GitHub Actions, test matrix, release pipelines
6. **Cloud** — AWS `boto3` basics, S3, Lambda packaging, IaC overview

**Capstone DV:** Library published to PyPI + containerized microservice deployed via CI.

---

## Track E — Security & Reliability Engineering

1. **Secure Coding** — validation, escaping, secrets handling
2. **Crypto 101** — hashing, HMAC, Fernet, key rotation basics
3. **Supply Chain** — `pip-audit`/`safety`, lockfiles, hash pinning
4. **Observability** — structured logs, tracing (OpenTelemetry), metrics
5. **Resilience** — retries, bulkheads, circuit breakers, chaos basics
6. **Testing** — fuzzing, property-based testing at boundaries

**Capstone SR:** Hardening an API service with audits, rate-limits, alerts, SLOs.

---

# Advanced Topics & Internals (post-specialization)

1. **Performance** — profiling (`cProfile`, `line_profiler`), `tracemalloc`, hot paths
2. **Compiled Speedups** — Cython, Numba, PyPy overview
3. **C Extensions** — CPython C-API, pybind11
4. **Internals** — bytecode (`dis`), refcounting & GC, descriptor protocol deep dive
5. **Metaprogramming** — metaclasses, import hooks, AST transforms (overview)

**Capstone AI:** Implement a tiny DSL that compiles to Python AST and executes.

---

# Portfolio & Capstones (choose several)

1. **CLI Suite** — cross-platform, typed, tested, packaged, and released.
2. **FastAPI Service** — JWT auth, DB, caching, background jobs, observability.
3. **Data Project** — reproducible notebook → package → report/dashboard.
4. **Automation** — weekly ETL with proper logging & alerting.
5. **Open Source** — contribute docs/tests/features to a library you use.

**Milestone MP:** Recruiter-ready GitHub with READMEs, tests, CI badges, and screenshots.

---

# Assessment Checkpoints (self-evaluate)

* **After Phase 1:** Write non-trivial scripts without Googling syntax.
* **After Phase 3:** Explain data model methods and tradeoffs of inheritance vs composition.
* **After Phase 4:** CI blocks on lint, type, and tests; you fix failures quickly.
* **After Phase 6:** Choose concurrency model by evidence (benchmarks).
* **After Phase 8:** Ship an API other devs can use with minimal hand-holding.
* **After any Track:** Deploy something real, gather feedback, iterate.

---

# Practice Cadence (repeat weekly)

1. **Read**: 1 doc chapter + 1 PEP skim.
2. **Code**: build a small feature or bugfix.
3. **Reflect**: log 2–3 lessons & anti-patterns.
4. **Share**: write a README snippet or blog post.

---

# Common Pitfalls (and fixes)

* **Skipping fundamentals** → Do Phase 1 thoroughly; revisit as needed.
* **No tests** → Start testing in Phase 4; keep tests close to code.
* **One giant script** → Move to `src/` packages early, expose CLIs.
* **Ignoring types** → Add hints gradually; enforce in CI.
* **Premature async** → Profile first; only add complexity with evidence.
* **Secret leakage** → Use env vars and secret managers; never hardcode.

---

## Suggested Study Timeline (adapt as needed)

* **Phases 0–2:** Foundations & stdlib competency.
* **Phases 3–5:** Design, types, advanced language features.
* **Phases 6–8:** Concurrency, persistence, APIs.
* **Tracks A–E:** Specialize and deliver production projects.
* **Advanced/Internals:** Optimize, extend, and contribute upstream.

---

### How to Use This Roadmap

* Treat each phase as a checklist.
* Ship a small project at the end of every phase.
* Keep everything in one monorepo (subfolders per project) for a tidy portfolio.

> When you’re ready, we can tailor this to your background (e.g., web dev focus vs data science) and convert it into week-by-week goals with specific project briefs.
