import os
from dotenv import load_dotenv

load_dotenv()
from typing import Annotated
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import HumanMessage, SystemMessage


# 1. State schema for messages
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


model = ChatGroq(model="openai/gpt-oss-120b", api_key=os.getenv("GROQ_API_KEY"))


# 2. Tool functions
def add(a: int, b: int) -> int:
    """Add two numbers a and b."""
    return a + b


def sub(a: int, b: int) -> int:
    """Subtract two numbers a and b."""
    return a - b


tools = [add, sub]
model_with_tools = model.bind_tools(tools)


# 3. Model Node (returns dict update to messages)
def call_model(state: AgentState):
    response = model_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# 4. Build graph
graph = StateGraph(AgentState)

graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "agent")
# tools_condition is passed to conditional edges, NOT added via add_node()
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

app = graph.compile()

# Invoke
messages = [
    SystemMessage(content="You are a math assistant. Use tools for calculations."),
    HumanMessage(content="Perform addition of 90 and 80"),
]
response = app.invoke({"messages": messages})

for m in response["messages"]:
    m.pretty_print()
