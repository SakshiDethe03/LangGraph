from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def node_1(state: State):
    return {"graph_state": state['graph_state'] + " I am"}

def node_2(state: State):
    return {"graph_state": state['graph_state'] + " happy!"}

def node_3(state: State):
    return {"graph_state": state['graph_state'] + " so happy!"}

builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()

