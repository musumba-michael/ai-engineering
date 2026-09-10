"""01-nodes.ipynb — a calculator chain: one node per operation."""

import operator
from typing import Annotated

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class Pipeline(TypedDict):
    value: float
    steps: Annotated[list[str], operator.add]


def add_ten(state: Pipeline) -> dict:
    new = state["value"] + 10
    return {"value": new, "steps": ["+10"]}


def double(state: Pipeline) -> dict:
    new = state["value"] * 2
    return {"value": new, "steps": ["x2"]}


def subtract_three(state: Pipeline) -> dict:
    new = state["value"] - 3
    return {"value": new, "steps": ["-3"]}


builder = StateGraph(Pipeline)
builder.add_node(add_ten)
builder.add_node(double)
builder.add_node(subtract_three)

builder.add_edge(START, "add_ten")
builder.add_edge("add_ten", "double")
builder.add_edge("double", "subtract_three")
builder.add_edge("subtract_three", END)

graph = builder.compile()
