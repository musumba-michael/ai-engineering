"""06-tools.ipynb — tools called directly with .invoke(), no model involved.

`ToolNode` is not used here: it reads tool calls off an AIMessage, and there is no
model in this notebook to produce one. Pick an op in Studio and the node invokes the
matching tool itself.
"""

import operator
from typing import Annotated, Literal

from langchain.tools import tool
from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def safe_divide(a: float, b: float) -> str:
    """Divide a by b. Returns an error message if b is zero."""
    if b == 0:
        return "Error: cannot divide by zero."
    return str(a / b)


TOOLKIT = {t.name: t for t in [add, subtract, multiply, safe_divide]}


class Calculator(TypedDict):
    a: float
    b: float
    op: Literal["add", "subtract", "multiply", "safe_divide"]
    result: str
    steps: Annotated[list[str], operator.add]


def run_tool(state: Calculator) -> dict:
    chosen = TOOLKIT[state["op"]]
    result = chosen.invoke({"a": state["a"], "b": state["b"]})
    return {
        "result": str(result),
        "steps": [f"{state['op']}({state['a']}, {state['b']}) -> {result}"],
    }


builder = StateGraph(Calculator)
builder.add_node("run_tool", run_tool)
builder.add_edge(START, "run_tool")
builder.add_edge("run_tool", END)

graph = builder.compile()
