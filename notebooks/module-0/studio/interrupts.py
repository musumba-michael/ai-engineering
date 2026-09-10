"""05-interrupts.ipynb — pause when the sides do not form a triangle.

Try sides [2, 3, 9]: the run pauses and asks for a shorter longest side. Resume with
a value (e.g. 4) and it classifies as scalene.
"""

import operator
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt
from typing_extensions import TypedDict


class Triangle(TypedDict):
    sides: list[float]
    notes: Annotated[list[str], operator.add]


def measure_and_classify(
    state: Triangle,
) -> Command[Literal["equilateral", "isosceles", "scalene"]]:
    a, b, c = sorted(state["sides"])

    if a + b <= c:
        c = interrupt(f"{a}, {b}, {c} is not a triangle: {a} + {b} <= {c}. Give a shorter longest side.")

    sides = sorted([a, b, c])
    distinct = len(set(sides))
    kind = "equilateral" if distinct == 1 else "isosceles" if distinct == 2 else "scalene"

    return Command(update={"sides": sides, "notes": [f"sides {sides}"]}, goto=kind)


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
builder.add_edge("equilateral", END)
builder.add_edge("isosceles", END)
builder.add_edge("scalene", END)

graph = builder.compile()
