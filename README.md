# ai-engineering

A [Turborepo](https://turborepo.dev) monorepo combining TypeScript apps and Python
packages in a single task graph. Node workspaces are managed by
[pnpm](https://pnpm.io); Python workspaces by [uv](https://docs.astral.sh/uv/),
wired into Turborepo through the `experimentalPythonWorkspaces` future flag.

```
ai-engineering/
├── apps/
│   ├── api/        Django REST service        (Python, uv)
│   ├── web/        Next.js app  :3000         (TypeScript)
│   └── docs/       Next.js app  :3001         (TypeScript)
├── notebooks/      Jupyter + LangGraph        (Python, uv)
├── packages/
│   ├── ui/                 shared React components
│   ├── eslint-config/      shared ESLint config
│   └── typescript-config/  shared tsconfig
├── devbox.json     toolchain (uv, node, pnpm, turbo)
├── turbo.json      task graph
├── pyproject.toml  uv workspace root
└── uv.lock         single lockfile for all Python members
```

## 1. Install Devbox

Every tool this repo needs `uv`, `node`, `pnpm`, `turbo` is pinned in
[devbox.json](devbox.json), so Devbox is the only thing you install by hand.

Devbox is built on [Nix](https://nixos.org), which the install script sets up for
you if it isn't present. On macOS and Linux:

```sh
curl -fsSL https://get.jetify.com/devbox | bash
```

On Windows, install it inside [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install).

Then enter the environment from the repo root:

```sh
devbox shell
```

Your prompt gains a `(devbox)` prefix. The first run downloads the toolchain and
takes a few minutes; later runs are instant. Leave with `exit`.

> Every command below assumes you are inside `devbox shell`.

## 2. Install dependencies

```sh
pnpm install     # Node workspaces
uv sync          # Python workspaces (creates ./.venv)
```

## 3. Configure secrets

One `.env` at the repo root serves the whole monorepo. Copy
[.env.example](.env.example) and fill in your keys:

```sh
cp .env.example .env
```

---

## Commands

We are using [Turborepo](https://turborepo.dev) as our task runner. Every task is defined
in [turbo.json](turbo.json) and runs the same way whether it is TypeScript or
Python work.

### Examples

| What you want | Command |
| --- | --- |
| JupyterLab (`:8888`) | `turbo run dev --filter=notebooks` |
| LangGraph Studio (`:2024`) | `turbo run studio --filter=notebooks` |
| Django dev server (`:8000`) | `turbo run dev --filter=api` |
| Next.js web (`:3000`) | `turbo run dev --filter=web` |
| Everything in dev at once | `turbo run dev` |
| Lint (ruff + eslint) | `turbo run lint` |
| Test | `turbo run test` |
| Format | `turbo run format` |
| Build | `turbo run build` |
| Verify `uv.lock` is current | `turbo run check` |

`turbo run dev` with no filter starts web on `:3000`, docs on `:3001`, Django on
`:8000` and JupyterLab on `:8888` together.

Re-resolving the Python lockfile is a plain uv command, not a turbo task:

```sh
uv lock
```

### What each turbo task expands to

Python tasks are registered automatically by the `experimentalPythonWorkspaces`
flag there are no `scripts` to declare, because uv has no task runner. Turbo
detects the tools each member declares and maps them:

| Task | Package | Runs |
| --- | --- | --- |
| `build` | `web`, `docs` | `next build` |
| `lint` | `web`, `docs`, `@repo/ui` | `eslint` |
| `lint` | `api` | `uv run --frozen --package api ruff check apps/api` |
| `test` | `api` | `uv run --frozen --package api pytest apps/api` |
| `format` | `api` | `ruff format` |
| `format` | `notebooks` | `uv format -- notebooks` |
| `check` | workspace root | `uv lock --check` |
| `check-types` | `web`, `docs`, `@repo/ui` | `tsc --noEmit` |
| `dev` | `notebooks` | `uv run --package notebooks jupyter lab` |
| `dev` | `api` | `uv run --package api python manage.py runserver` |
| `studio` | `notebooks` | `uv run --package notebooks langgraph dev` |

Filter any task to one package with `--filter=<name>`, and pass arguments through
to the underlying tool after `--`:

```sh
turbo run lint --filter=api -- --fix
turbo run test --filter=api -- -k smoke
```

### Adding a command

`pyproject.toml` cannot hold script aliases uv has no task-runner equivalent of
`package.json` scripts ([astral-sh/uv#5903](https://github.com/astral-sh/uv/issues/5903)),
and `[project.scripts]` declares Python entry points, not shell commands. Define
new commands in `turbo.json` instead, using `experimentalTaskCommand`:

```json
"notebooks#studio": {
  "command": ["uv", "run", "--package", "notebooks", "langgraph", "dev"],
  "cache": false,
  "persistent": true
}
```

Package-scoped commands run with their package directory as the working
directory.

---

## How the Python side fits together

- The uv workspace root is [pyproject.toml](pyproject.toml); its members are
  `apps/api` and `notebooks`.
- All members share **one** [uv.lock](uv.lock), so every package resolves to the
  same version of every dependency. There is no catalog to maintain when
  `notebooks` and `api` both use LangChain, the lockfile guarantees they agree.
- Both members set `package = false`: they are applications to run, not libraries
  to publish, so nothing is built or installed for them.
- Adding a member means creating its `pyproject.toml`, listing it under
  `[tool.uv.workspace] members`, and running `uv lock`.

## Per-package docs

- [apps/api/README.md](apps/api/README.md) -> Django service
- [notebooks/README.md](notebooks/README.md) -> Jupyter and LangGraph Studio
