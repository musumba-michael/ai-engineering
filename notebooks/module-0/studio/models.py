"""07-models.ipynb — a model node with the calculator tools bound.

The only module-0 graph that needs an API key.
"""

from typing import Annotated

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langgraph.graph import END, START, StateGraph, add_messages
from typing_extensions import TypedDict


@tool
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@tool
def divide(a: float, b: float) -> float:
    """Divide a by b."""
    return a / b


model = init_chat_model("openai:gpt-4o-mini", temperature=0)
with_tools = model.bind_tools([add, multiply, divide])


class ChatState(TypedDict):
    messages: Annotated[list, add_messages]


def calculator(state: ChatState) -> dict:
    """A node whose entire job is one model call."""
    return {"messages": [with_tools.invoke(state["messages"])]}


builder = StateGraph(ChatState)
builder.add_node("calculator", calculator)
builder.add_edge(START, "calculator")
builder.add_edge("calculator", END)

graph = builder.compile()
