from langgraph.graph import StateGraph, END

from core.state import AppState
from core.schemas import Intent

from core.nodes.router import router_node
from core.nodes.chat import chat_node
from core.nodes.context import context_node
from core.nodes.extraction import extraction_node


def should_extract(state: AppState) -> str:
    if state["intent"] == Intent.REVIEW:
        return "extraction"
    return "end"


builder = StateGraph(AppState)

builder.add_node("router", router_node)
builder.add_node("chat", chat_node)
builder.add_node("context", context_node)
builder.add_node("extraction", extraction_node)

builder.set_entry_point("router")

builder.add_edge("router", "context")
builder.add_edge("context", "chat")

builder.add_conditional_edges(
    "chat",
    should_extract,
    {
        "extraction": "extraction",
        "end": END,
    },
)
builder.add_edge("extraction", END)

graph = builder.compile()