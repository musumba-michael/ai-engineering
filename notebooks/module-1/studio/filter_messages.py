"""06-trim-filter-messages.ipynb — drop all but the two most recent messages."""

from langchain_core.messages import RemoveMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, MessagesState, StateGraph

llm = ChatGroq(model="openai/gpt-oss-20b")


# Nodes
def filter_messages(state: MessagesState):
    # Delete all but the 2 most recent messages
    delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
    return {"messages": delete_messages}


def chat_model_node(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}


# Build graph
builder = StateGraph(MessagesState)
builder.add_node("filter", filter_messages)
builder.add_node("chat_model", chat_model_node)
builder.add_edge(START, "filter")
builder.add_edge("filter", "chat_model")
builder.add_edge("chat_model", END)

graph = builder.compile()
