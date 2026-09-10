"""04-memory.ipynb — a running total that survives across runs.

Studio supplies the checkpointer, so re-running on the same thread keeps adding to
the total instead of starting from zero.
"""

import operator
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class Calculator(TypedDict):
    total: float
    amount: float
    history: Annotated[list[str], operator.add]


def add_amount(state: Calculator) -> dict:
    total = state.get("total", 0)
    new_total = total + state["amount"]
    return {
        "total": new_total,
        "history": [f"{total} + {state['amount']} = {new_total}"],
    }


builder = StateGraph(Calculator)
builder.add_node("add_amount", add_amount)
builder.add_edge(START, "add_amount")
builder.add_edge("add_amount", END)

graph = builder.compile()
