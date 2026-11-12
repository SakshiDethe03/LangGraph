import random
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    graph_state: str

def router(state: State):
    return {"graph_state": state['graph_state'] + " I am"}

def positive(state: State):
    return {"graph_state": state['graph_state'] + " Happy!"}

def negative(state: State):
    return {"graph_state": state['graph_state'] + " sad!"}

def decide_mood(state: State) -> Literal["positive", "negative"]:
    if random.random() < 0.5:
        return "positive"
    return "negative"

builder = StateGraph(State)
builder.add_node("router", router)
builder.add_node("positive", positive)
builder.add_node("negative", negative)

builder.add_edge(START, "router")
builder.add_conditional_edges("router", decide_mood)
builder.add_edge("positive", END)
builder.add_edge("negative", END)

graph = builder.compile()

