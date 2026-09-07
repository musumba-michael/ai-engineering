# api

Django REST service. A member of the uv workspace defined at the repo root.

```
apps/api/
├── core/           Django project (settings, urls, asgi, wsgi)
├── manage.py
└── pyproject.toml  dependencies (no build backend — package = false)
```

## Running

From anywhere in the repo, inside `devbox shell`:

```sh
turbo run dev --filter=api        # → http://localhost:8000
```

Or directly:

```sh
cd apps/api
uv run python manage.py runserver
```

Any `manage.py` subcommand works the same way — `uv run python manage.py migrate`,
`... createsuperuser`, and so on. `uv run` resolves the workspace environment, so
there is no virtualenv to activate.

## Turbo tasks

| Task | Runs |
| --- | --- |
| `turbo run dev --filter=api` | `uv run --package api python manage.py runserver` |
| `turbo run lint --filter=api` | `uv run --frozen --package api ruff check apps/api` |
| `turbo run test --filter=api` | `uv run --frozen --package api pytest apps/api` |
| `turbo run format --filter=api` | `ruff format` |

Arguments pass through after `--`:

```sh
turbo run lint --filter=api -- --fix
turbo run test --filter=api -- -k smoke
```

There is no `build` task: `package = false` in `pyproject.toml`, because this is a
service you run rather than a library you publish, so there is no wheel to
produce. If you later deploy by building an artifact, define a `build` command in
the root `turbo.json` under `experimentalTaskCommand`.

## Tests

`pytest` is configured through `[tool.pytest.ini_options]` in
[pyproject.toml](pyproject.toml), with `pytest-django` supplying the
`DJANGO_SETTINGS_MODULE` and fixtures such as `client`. Tests belong in
`apps/api/tests/`.

> **Note:** `tests/` is currently empty, so `turbo run test` fails with exit code
> 5 (`no tests ran`). Add a test, or drop the pytest config and the
> `pytest`/`pytest-django` dev dependencies if you would rather not have a test
> task registered yet.

## Dependencies

Edit `[project.dependencies]` in [pyproject.toml](pyproject.toml), then re-lock
from the repo root:

```sh
uv lock
```

LangChain packages can be added here directly — the shared workspace lockfile
keeps their versions identical to whatever `notebooks/` resolves.
