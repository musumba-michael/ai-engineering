"""05-state-schema.ipynb — separate input, output and internal state schemas.

`notes` is internal: it is written by `thinking_node` and never leaves the graph,
because `output_schema` only exposes `answer`.
"""

from langgraph.graph import END, START, StateGraph
from typing_extensions import TypedDict


class InputState(TypedDict):
    question: str


class OutputState(TypedDict):
    answer: str


class OverallState(TypedDict):
    question: str
    answer: str
    notes: str


def thinking_node(state: InputState):
    return {"answer": "bye", "notes": "... his name is Lance"}


def answer_node(state: OverallState) -> OutputState:
    return {"answer": "bye Lance"}


builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
builder.add_node("thinking_node", thinking_node)
builder.add_node("answer_node", answer_node)

builder.add_edge(START, "thinking_node")
builder.add_edge("thinking_node", "answer_node")
builder.add_edge("answer_node", END)

graph = builder.compile()
