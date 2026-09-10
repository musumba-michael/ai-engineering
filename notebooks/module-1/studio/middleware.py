"""10-middleware.ipynb — web search + SQL agent, gated by human approval."""

from pathlib import Path
from typing import Any, Callable, Dict

from langchain.agents import AgentState, create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelRequest,
    ModelResponse,
    after_agent,
    before_agent,
    wrap_model_call,
)
from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langgraph.runtime import Runtime
from tavily import TavilyClient

tavily_client = TavilyClient()

DB_PATH = Path(__file__).parent.parent / "resources" / "Chinook.db"
db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")


@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)


@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries"""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"


@before_agent
def log_before_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"[before_agent] run starting with {len(state['messages'])} message(s)")
    return None


@after_agent
def log_after_agent(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    print(f"[after_agent] run finished with {len(state['messages'])} message(s)")
    return None


@wrap_model_call
def trace_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    print("[wrap_model_call] -> calling the model")
    response = handler(request)
    print("[wrap_model_call] <- model returned")
    return response


# Studio supplies its own checkpointer, so none is passed here.
graph = create_agent(
    model="gpt-5-nano",
    tools=[web_search, sql_query],
    middleware=[
        log_before_agent,
        trace_model,
        HumanInTheLoopMiddleware(
            interrupt_on={"sql_query": True, "web_search": True},
        ),
        log_after_agent,
    ],
)
