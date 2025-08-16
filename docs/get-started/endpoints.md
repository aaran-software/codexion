# Personal Coding Assistant — Project Blueprint & Monorepo

A full-stack, extensible personal coding assistant focused on **codebase-scale memory**, **local-first search**, **safe refactors (ReSharper-like)**, and **agentic workflows**. Built with **Python (backend/agents)** and **React (web UI)**. Optional VS Code extension + CLI.

---

## 0) Goals & Capabilities

* **Understands entire repo**: ingest, index, and keep code in memory; incremental updates on git changes.
* **Local-first retrieval**: symbol/AST index + embeddings + TF‑IDF; fallback to web search if confidence low; otherwise ask LLM to clarify.
* **Safe refactors**: plan → patch → compile/test → review → apply. Supports rename, extract, dead code detection, dependency pruning, API upgrade, codemods.
* **AI agents**: planner, code analyst, refactorer, test writer, doc writer, researcher. Deterministic tool calls + human-in-the-loop gates.
* **Surfaces diffs**: explain changes, show risk estimate, link to tests.
* **Privacy-first**: local vector DB; controllable redaction when calling cloud LLMs; model routing to local LLM where possible.

---

## 1) Architecture Overview

**Monorepo** with shared packages and isolated services:

```
personal-coding-assistant/
├─ apps/
│  ├─ api/                    # FastAPI service (Python)
│  ├─ web/                    # React app (Vite or Next.js)
│  ├─ vscode-ext/             # VS Code extension (TypeScript)
│  └─ cli/                    # Python CLI (Typer)
├─ services/
│  ├─ indexer/                # Incremental code indexer + watchers
│  ├─ agents/                 # Orchestrator & tool-executing agents
│  └─ executor/               # Sandbox runner for tests/builds
├─ packages/
│  ├─ py-shared/              # Shared Python utils (schemas, prompts)
│  ├─ ts-shared/              # Shared TS types (API client)
│  └─ codemods/               # Reusable refactor rules (libcst/ts-morph)
├─ data/
│  ├─ vectors/                # Local vector store (FAISS/Chroma)
│  ├─ ast/                    # AST snapshots / symbol DB (SQLite)
│  └─ cache/                  # Tool and web cache
├─ .github/workflows/         # CI (lint, typecheck, tests)
├─ docker/                    # Optional containers for services
├─ scripts/                   # Dev scripts (bootstrap, index)
└─ README.md
```

### Core Data Flows

1. **Ingest → Index**

   * File watcher detects changes → tokenizer → language router → AST builder (libcst for Python, ts-morph for TS/JS, tree-sitter fallback) → symbols & references → embeddings → store.
2. **Query → Retrieve**

   * Hybrid retrieval: BM25/TF‑IDF + dense vectors + symbol graph ranking → unified candidates → confidence score.
3. **Plan → Act (Agents)**

   * Planner decomposes task; tools: search\_symbols, read\_files, generate\_patch, run\_tests, create\_pr.
4. **Guardrails**

   * Static checks (ruff/mypy, eslint/tsc) → unit tests → semantic diff checks.
5. **Explain → Approve**

   * React UI & VS Code extension present diffs, safety score, and test results; user approves to apply.

---

## 2) Technology Choices

* **Backend**: Python 3.11, FastAPI, Uvicorn.
* **Indexing**: tree-sitter (multi-language), libcst (safe Python edits), ts-morph (TS/JS), ripgrep for raw search.
* **Embeddings**: `sentence-transformers` (local) or OpenAI text-embedding-3-small (configurable). Store with **FAISS** or **Chroma**.
* **Symbol/AST DB**: SQLite (local), with FTS5 for text + tables for symbols, refs, defs.
* **LLMs**: pluggable — local (Ollama: Llama 3.x, Qwen, Mistral) and cloud (GPT-4.1/4o, Claude). Router based on task + token budget + privacy rules.
* **Agents/Orchestration**: Pydantic tool schemas + function calling; Guardrails with jsonschema.
* **Sandbox**: pytest / npm test in ephemeral venv/node env; resource caps.
* **UI**: React (Vite), shadcn/ui, Monaco editor, diff viewer (react-diff-viewer), charts (recharts).
* **Extension**: VS Code using Language Server Protocol bridges (custom code actions via RPC to API).

---

## 3) Local-First Search → Web Fallback Policy

1. **Try local**: hybrid retrieval from vectors + BM25 + symbol index. If score `S ≥ τ_local`, answer/refactor locally.
2. **If `S < τ_local`**: ask clarifying question *or* perform scoped web search (Bing/Tavily) with code-safe redaction.
3. **Caching**: persist web answers with provenance; show citations in UI.
4. **User override**: per-task toggle: Local only / Allow web / Cloud LLM allowed.

---

## 4) ReSharper‑style Refactors (MVP Set)

* **Rename Symbol** (project-wide) with reference graph.
* **Extract Method/Function** with usage update.
* **Inline Variable** / **Introduce Variable**.
* **Dead Code Elimination** (unreferenced symbols, feature flags).
* **Import Cleanup & Dep Prune**.
* **API Migration** rules (codemods directory).
* **Docstring/JSDoc generation** linked to symbols.

**Safety pipeline**: codemod → compile/typecheck → unit tests → risk score (changed public API? fan-out?) → present diff.

---

## 5) Agents & Tools

### Agents

* **Planner**: converts user goal → steps (schema: `PlanStep[]`).
* **Code Analyst**: reads candidates, builds context windows, chooses refactors or Q\&A.
* **Refactorer**: applies codemods/AST transforms; generates patches.
* **Test Writer**: adds/updates tests; ensures coverage for touched modules.
* **Researcher**: web search + summarize with citations when allowed.
* **Explainer**: human-readable writeups & commit messages.

### Tooling API (function-call schemas)

* `search_symbols(query, lang?, limit)`
* `read_files(paths[])`
* `retrieve_snippets(q, k)`
* `apply_codemod(name, params)`
* `generate_patch(edits[])`  → unified diff
* `run_tests(paths?, watch=false)`
* `static_check(target)` (ruff/mypy/eslint/tsc)
* `web_search(q)` (with redaction)
* `open_pr(branch, title, body)`

---

## 6) API Design (FastAPI)

```
POST /v1/query                 # ask, refactor, explain
POST /v1/index/scan            # full scan; returns repo stats
POST /v1/index/update          # file diff update
GET  /v1/search                # local hybrid search
POST /v1/patch/plan            # propose refactor plan
POST /v1/patch/apply           # apply patch to working tree
POST /v1/tests/run             # run tests sandboxed
GET  /v1/memory/item           # get project memory
POST /v1/memory/item           # upsert long-term fact
POST /v1/config                # set privacy/model routing
```

### Schemas (selected)

```json
// SearchResult
{
  "path": "src/app/foo.py",
  "symbol": "Foo.bar",
  "kind": "method",
  "score": 0.83,
  "start": 120,
  "end": 211
}

// Patch
{
  "branch": "feat/refactor-rename-foo",
  "diff": "--- a/src/foo.py\n+++ b/src/foo.py\n@@ ...",
  "checks": {"tests": "pass", "static": ["ruff:ok", "mypy:ok"]}
}
```

---

## 7) Data Model

* **tables**

  * `files(path, lang, hash, size, mtime)`
  * `symbols(id, path, name, kind, range, signature)`
  * `refs(symbol_id, from_path, range, kind)`
  * `embeddings(doc_id, vector, meta)` (FAISS index on disk)
  * `snippets(id, path, text, hash)` (FTS5)
  * `mem_kv(key, value, tags, updated_at)`
* **indexes**: FTS5 on snippets; btree on `symbols(name)`, `refs(symbol_id)`.

---

## 8) Privacy & Model Routing

* **Policies** per workspace: `{allowCloudLLM, allowWeb, redactPatterns, modelPrefs}`.
* **Redaction**: strip secrets via regex (keys, tokens, emails), and path-based ignore.
* **Routing**: small/local model for retrieval, cloud for reasoning-heavy if allowed; cost & token budget estimator.

---

## 9) UI/UX (React)

* **Panels**: Search, Symbols, Context, Diff, Tests, Planner.
* **Flows**:

  1. Enter goal → plan appears → choose steps → generate patch → preview diff → run checks → approve & apply.
  2. Ask question → citations (local files first), expandable snippets.
* **Components**: Monaco editor, Diff viewer, Tooltip risk meter, Trace panel (tool calls), Toggle (Local/Web/Cloud).

---

## 10) VS Code Extension

* Commands: "Assistant: Ask", "Assistant: Refactor Current Symbol", "Assistant: Explain Diff", "Assistant: Write Tests".
* Inline code actions powered by our API; shows plan & diff, applies edits via WorkspaceEdit.
* Background index sync via file watcher; status bar for retrieval confidence.

---

## 11) Initial Repo Scaffolds (key files)

### `apps/api/pyproject.toml`

```toml
[project]
name = "assistant-api"
version = "0.1.0"
dependencies = [
  "fastapi", "uvicorn[standard]", "pydantic", "sqlmodel", "aiosqlite",
  "sentence-transformers", "faiss-cpu", "scikit-learn", "tree_sitter", "libcst",
  "tiktoken", "python-dotenv", "httpx", "typer"
]
```

### `apps/api/main.py` (skeleton)

```python
from fastapi import FastAPI
from routes import search, index, patch, tests, query, memory

app = FastAPI(title="Personal Coding Assistant API")
app.include_router(search.router, prefix="/v1")
app.include_router(index.router,  prefix="/v1")
app.include_router(patch.router,  prefix="/v1")
app.include_router(tests.router,  prefix="/v1")
app.include_router(query.router,  prefix="/v1")
app.include_router(memory.router, prefix="/v1")

@app.get("/")
def ok():
    return {"ok": True}
```

### `services/indexer/worker.py` (outline)

```python
# Watches repo; builds AST, symbols, embeddings; writes SQLite + FAISS
```

### `services/agents/orchestrator.py` (outline)

```python
# Planner → tool calls → guardrails → patch proposal
```

### `apps/web/` (Vite + React + shadcn/ui + Monaco)

* Pages: `/search`, `/refactor`, `/tests`, `/settings`.
* Components: `CodeView`, `DiffPanel`, `PlanSteps`, `RetrievalDebug`, `RiskMeter`.

### `apps/vscode-ext/` (TypeScript)

* `extension.ts` registers commands; talks to API; shows webview for plan/diff.

### `apps/cli/` (Typer)

* `assist ask`, `assist refactor --rename Foo Bar`, `assist index`.

---

## 12) Retrieval Details (Hybrid Ranking)

Score = `w_sym*sym_sim + w_vec*vector_sim + w_bm25*bm25 + w_path*path_prior`

* Symbol sim from reference graph Jaccard.
* Vector sim from FAISS; normalize cosine.
* BM25 via FTS5 or `rank-bm25`.
* Path prior boosts nearby files to the active file.
* Calibrate weights with offline eval set.

---

## 13) Patching & Safety

* Patches generated as unified diffs.
* Static checks: ruff+flake8+mypy / eslint+tsc.
* Tests in sandbox with timeout; capture coverage delta.
* Block apply if public API changed without major version flag (configurable).

---

## 14) Prompts (abridged)

* **System**: "You are a coding assistant with tool access. Prefer local search; never fabricate paths; output diffs in unified format when asked to edit."
* **Planner**: expects JSON `PlanStep[]` with `tool` and `inputs`.
* **Refactorer**: "Given AST + constraints, produce `edits[]` with exact ranges; avoid broad regex."
* **Researcher**: "Only search web if local confidence < τ or user allows. Include citations."

---

## 15) Milestones & Roadmap

1. **MVP (2–3 weeks)**

   * Repo ingest (Python/TS), FAISS embeddings, FTS5 text index, basic search API.
   * React UI: search + snippet viewer; confidence score.
   * Agent: Planner + Code Analyst; Q\&A over repo.
2. **Refactor Phase**

   * libcst + ts-morph codemods; rename/extract/import cleanup; diff UI; tests runner.
3. **VS Code & CLI**

   * Inline actions; apply patches; background index sync.
4. **Safety & Research**

   * Static checks, coverage; web fallback with redaction; provenance in UI.
5. **Advanced**

   * API migrations, dep pruning, doc generation; PR creator; multi-repo workspaces.

---

## 16) Local Dev & Run

```bash
# Bootstrap
python -m venv .venv && source .venv/bin/activate
pip install -e apps/api
pip install -r apps/api/requirements.txt  # if you split deps
pnpm -C apps/web install

# Start services
uvicorn apps.api.main:app --reload --port 8000
pnpm -C apps/web dev

# Index current repo
python services/indexer/worker.py --path .
```

---

## 17) Config & Secrets

* `.env`: model keys (optional), search key, privacy flags.
* `config.yaml`: thresholds, model routing, ignore globs, redaction patterns.

---

## 18) Testing & Evaluation

* Golden Q\&A set per repo.
* Refactor correctness: compile success, tests pass, semantic equivalence checks (pyre/pyright where applicable).
* Retrieval quality: recall\@k on symbol-annotated queries.

---

## 19) License & Contributions

* MIT for code; include `SECURITY.md` (no code exfiltration) and `PRIVACY.md` (local-first policy).

---

## 20) Next Steps

* Pick **Vite or Next.js** for the web app.
* Confirm your **LLM providers** (local via Ollama? cloud fallback?).
* Tell me your **primary languages** (Python/TS/Java/Go) so I prioritize indexers.
* I can now generate the initial repo files (scaffolds) and a minimal working MVP.
