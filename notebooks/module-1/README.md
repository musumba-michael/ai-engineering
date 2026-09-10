# module-1 — messages, agents, and state

Eleven notebooks building from a message chain up to a middleware-wrapped agent.
Content is copied verbatim from the source courses, with one exception; see
**Provenance** below for what came from where.

Assumes [module-0](../module-0/README.md) — nodes, state, edges, memory, interrupts,
tools, models.

```
module-1/
├── 01-chain.ipynb                  messages as state, chat models, tools
├── 02-router.ipynb                 ToolNode + tools_condition
├── 03-agent.ipynb                  the ReAct loop
├── 04-agent-memory.ipynb           MemorySaver and threads
├── 05-state-schema.ipynb           schemas + reducers + multiple schemas   (3 combined)
├── 06-trim-filter-messages.ipynb   filtering, trimming, RemoveMessage
├── 07-chatbot-summarization.ipynb  summarization + external SQLite memory  (2 combined)
├── 08-prompting.ipynb              system prompts, few-shot, structured output
├── 09-multimodal-messages.ipynb    text, image, and audio input
├── 10-mcp.ipynb                    local and hosted MCP servers
├── 11-middleware.ipynb             hooks, wrappers, and human-in-the-loop
├── resources/                      assets the notebooks load
└── studio/                         graphs served by LangGraph Studio
```

## Running

```sh
turbo run dev --filter=notebooks      # JupyterLab → http://localhost:8888
```

## API keys

Every notebook here calls a model — there is no key-free path through this module.

Each notebook loads the repo-root `.env` with a single cell, and nothing else:

```python
from dotenv import load_dotenv

load_dotenv()
```

`load_dotenv()` walks up from the notebook's directory and finds
`ai-engineering/.env` on its own, so there is no path to keep in sync and no
interactive prompt. Keys used: `OPENAI_API_KEY`, `TAVILY_API_KEY` (11 and the MCP
server), and `LANGSMITH_*` for tracing, which is on by default via the root `.env`.

`05-state-schema.ipynb` has no env cell because it never calls a model.

Notebooks 01–07 keep their original `%pip install` cells. They are redundant here —
everything is already in the uv environment — and harmless.

## Resources

| File | Used by |
| --- | --- |
| `resources/Chinook.db` | 11-middleware |
| `resources/2.1_mcp_server.py` | 10-mcp (the local stdio server) |
| `resources/moon.png` | 09-multimodal — upload it at the `FileUpload` widget |

## Dependencies added for this module

`langchain-mcp-adapters`, `mcp-server-time` (10-mcp); `tavily-python` (11-middleware
and the MCP server);
`ipywidgets` (09 image upload); `scipy`, `sounddevice`, `tqdm` (09 audio capture).
Already re-locked and synced — see [notebooks/pyproject.toml](../pyproject.toml).

`10-mcp.ipynb` launches its local server with `"command": "python"`, so the `python` on
`PATH` must be this repo's. Launching Jupyter through `turbo run dev --filter=notebooks`
(or `uv run`) guarantees that; a shell with another project's virtualenv activated does not.

The audio section of `09-multimodal` records from a microphone via `sounddevice`, and
needs `libportaudio` plus an input device. Skip it if you are running headless.

## LangGraph Studio

```sh
turbo run studio --filter=notebooks   # → http://localhost:2024
```

Seven graphs are registered in the shared [notebooks/langgraph.json](../langgraph.json).
Graph names are global across that one file, so every key is prefixed `module_1_`:

| Graph | File | From |
| --- | --- | --- |
| `module_1_chain` | `studio/chain.py` | 01 — model with a bound tool, no execution |
| `module_1_router` | `studio/router.py` | 02 — `tools_condition` routing |
| `module_1_agent` | `studio/agent.py` | 03, 04 — the ReAct loop |
| `module_1_state_schema` | `studio/state_schema.py` | 05 — separate input / output / internal schemas |
| `module_1_filter_messages` | `studio/filter_messages.py` | 06 — `RemoveMessage` filtering |
| `module_1_summarization` | `studio/summarization.py` | 07 — summarize past a message threshold |
| `module_1_prompting` | `studio/prompting.py` | 08 — few-shot prompt + structured output |
| `module_1_multimodal` | `studio/multimodal.py` | 09 — agent taking text and image blocks |
| `module_1_mcp` | `studio/mcp.py` | 10 — tools loaded from a local MCP server |
| `module_1_middleware` | `studio/middleware.py` | 11 — both tools, gated by approval |

Every notebook has a graph.

`router.py`, `agent.py` and `summarization.py` are the upstream langchain-academy studio
files, copied unchanged. The rest are lifted from the matching notebook.

Studio supplies its own checkpointer, so none of these compile with one — that is why
03 and 04 share a single graph.

**`mcp.py` uses an async graph factory.** Its tools have to be fetched over stdio
before the agent exists, and doing that at import time would spawn a subprocess while
the server is still loading modules — and a graph that fails to import takes down the
whole `langgraph dev` server, not just its own entry. So `langgraph.json` points at
`make_graph` rather than a `graph` variable, and the server awaits it at startup:

```python
async def make_graph(config=None):
    tools = await client.get_tools()
    return create_agent(model="gpt-5-nano", tools=tools, ...)
```

It also launches the server with `sys.executable` rather than `"python"`, so it does not
depend on which interpreter happens to be first on `PATH`.

`multimodal.py` accepts image content blocks, but the microphone section of notebook 09
has no Studio equivalent — recording audio is a client-side concern.

## Provenance

Copied without rewriting, so these stay diffable against their sources.

| Notebook | Source |
| --- | --- |
| 01–04 | `langchain-academy/module-1/{chain,router,agent,agent-memory}.ipynb` |
| 05 | `langchain-academy/module-2/{state-schema,state-reducers,multiple-schemas}.ipynb` |
| 06 | `langchain-academy/module-2/trim-filter-messages.ipynb` |
| 07 | `langchain-academy/module-2/{chatbot-summarization,chatbot-external-memory}.ipynb` |
| 08 | `lca-lc-foundations/notebooks/module-1/1.1_prompting.ipynb` |
| 09 | `lca-lc-foundations/notebooks/module-1/1.4_multimodal_messages.ipynb` |
| 10 | `lca-lc-foundations/notebooks/module-2/2.1_mcp.ipynb` |
| 11 | tools from `1.2_web_search.ipynb` + `bonus_sql.ipynb`; middleware written against the [docs](https://docs.langchain.com/oss/python/langchain/middleware) |

For the two combined notebooks (05 and 07), the first source keeps its Colab badge and
`%pip install` cell and the later sources have theirs dropped; every teaching cell is
untouched and in source order.

**11-middleware is the one notebook not copied.** It merges the web-search and SQL
agents into a single agent and then wraps it, because no source repo demonstrates
`before_model` / `after_model` / `wrap_model_call`. The two tool definitions are lifted
verbatim from `1.2_web_search.ipynb` and `bonus_sql.ipynb`; the middleware is written
against the installed langchain 1.4.0 API and verified by running the notebook.
