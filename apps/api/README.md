# api

Python package in the uv workspace, wired into Turborepo via
`futureFlags.experimentalPythonWorkspaces`.

```bash
turbo run check --filter=api      # uv check --frozen --package api
turbo run lint --filter=api       # ruff check
turbo run test --filter=api       # pytest
turbo run build --filter=api      # uv build --package=api
```
