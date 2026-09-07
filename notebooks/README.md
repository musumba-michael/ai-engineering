# notebooks

Jupyter notebooks and LangGraph Studio graphs for LangChain/LangGraph work. A
member of the uv workspace defined at the repo root.

```
notebooks/
├── module-0/
│   ├── basics.ipynb
│   └── studio/agent.py     graph served as `module_0`
├── module-1/studio/agent.py   graph served as `module_1`
├── module-2/studio/agent.py   graph served as `module_2`
├── langgraph.json          one config for every studio folder
└── pyproject.toml          dependencies (no build backend ie package = false)

(API keys live in the repo-root .env, not here.)
```

## Running

From anywhere in the repo, inside `devbox shell`:

```sh
turbo run dev --filter=notebooks      # JupyterLab           → http://localhost:8888
turbo run studio --filter=notebooks   # LangGraph dev server → http://localhost:2024
```

Both are defined in the repo-root `turbo.json` and run with `notebooks/` as their
working directory, which is how `langgraph dev` finds `langgraph.json`.

## Secrets

There is one `.env` for the whole monorepo, at the repo root.
`langgraph.json` declares `"env": "../.env"`, which resolves relative to the
config file and so reaches the root, nothing lives in `notebooks/`:

```sh
cp ../.env.example ../.env      # from the repo root: cp .env.example .env
```

## Adding a graph

[langgraph.json](langgraph.json) is a **single config covering every studio
folder**; you do not need one per module. Graph paths resolve relative to the
config file, so a path can reach into any subdirectory:

```json
{
  "graphs": {
    "module_0": "./module-0/studio/agent.py:graph",
    "module_1": "./module-1/studio/agent.py:graph",
    "module_2": "./module-2/studio/agent.py:graph"
  },
  "env": "../.env",
  "python_version": "3.12",
  "dependencies": ["."]
}
```

Two rules to respect:

1. **Graph names are global.** Every key in `graphs` must be unique across the
   whole file, so name them per module (`module_1_router`, not `router`). This is
   the one thing per-folder configs would give you for free.
2. **Every listed file must exist.** A single missing path fails the entire
   server with `GraphLoadError` not just that one graph so add an entry only
   once its file is there.

The `agent.py` files currently in each studio folder are working placeholders.
Replace the body with your real graph, keeping the module-level `graph` symbol
(or update `langgraph.json` to point at whatever you name it).

You would only want a separate `langgraph.json` per folder if a module needed
different dependencies, its own `.env`, or independent deployment.

## Dependencies

Edit `[project.dependencies]` in [pyproject.toml](pyproject.toml), then re-lock
from the repo root:

```sh
uv lock
```

The workspace shares one lockfile, so anything also used by `apps/api` resolves to
a single agreed version automatically.
