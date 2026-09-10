"""02-state.ipynb — a Pydantic state schema that validates its input.

Submit b = 0 in Studio and the run is rejected before any node executes.
"""

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, field_validator


class ModelState(BaseModel):
    a: float
    b: float
    result: float = 0.0

    @field_validator("b")
    @classmethod
    def not_zero(cls, v: float) -> float:
        if v == 0:
            raise ValueError("cannot divide by zero")
        return v


def divide(state: ModelState) -> dict:
    return {"result": state.a / state.b}


builder = StateGraph(ModelState)
builder.add_node("divide", divide)
builder.add_edge(START, "divide")
builder.add_edge("divide", END)

graph = builder.compile()
