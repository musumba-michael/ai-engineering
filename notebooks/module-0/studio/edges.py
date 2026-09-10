"""03-edges.ipynb — classify a triangle, routing from inside the node with Command."""

import operator
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from typing_extensions import TypedDict


class Triangle(TypedDict):
    sides: list[float]
    notes: Annotated[list[str], operator.add]


def measure_and_classify(
    state: Triangle,
) -> Command[Literal["equilateral", "isosceles", "scalene"]]:
    a, b, c = state["sides"]
    distinct = len({a, b, c})
    kind = "equilateral" if distinct == 1 else "isosceles" if distinct == 2 else "scalene"
    return Command(update={"notes": [f"sides {a}, {b}, {c}"]}, goto=kind)


def equilateral(state: Triangle) -> dict:
    return {"notes": ["equilateral: all three sides equal"]}


def isosceles(state: Triangle) -> dict:
    return {"notes": ["isosceles: exactly two sides equal"]}


def scalene(state: Triangle) -> dict:
    return {"notes": ["scalene: no two sides equal"]}


builder = StateGraph(Triangle)
builder.add_node("measure", measure_and_classify)
builder.add_node("equilateral", equilateral)
builder.add_node("isosceles", isosceles)
builder.add_node("scalene", scalene)

builder.add_edge(START, "measure")
# no edge out of "measure" — Command(goto=...) supplies it
builder.add_edge("equilateral", END)
builder.add_edge("isosceles", END)
builder.add_edge("scalene", END)

graph = builder.compile()
