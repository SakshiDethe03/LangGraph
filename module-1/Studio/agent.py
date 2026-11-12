import os
from dotenv import load_dotenv

load_dotenv()

from langsmith import traceable
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openrouter import ChatOpenRouter
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

api_key = os.getenv("OPENROUTER_API_KEY")

import warnings

warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings:",
    category=UserWarning,
)

llm = ChatOpenRouter(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    api_key=api_key,
)


@traceable(run_type="tool")
def add(a: int, b: int) -> int:
    """Performs Addition of a and b

    Arguments:
        a: first int
        b: second int
    """
    return a + b


def sub(a: int, b: int) -> int:
    """Performs Substraction of a and b

    Arguments:
        a: first int
        b: second int
    """
    return a - b


def multiply(a: int, b: int) -> int:
    """Performs multiplication of a and b

    Arguments:
        a: first int
        b: second int
    """
    return a * b


def div(a: int, b: int) -> int:
    """Performs division of a and b

    Arguments:
        a: first int
        b: second int
    """
    return a / b


tools = [add, sub, multiply, div]

llm_with_tools = llm.bind_tools(tools)

system_msg = SystemMessage(
    content="""You are a helpful assistant.
    Your task is to perform suitable arithmetic operations on the given inputs."""
)


@traceable
def assistant(state: MessagesState):
    result = {"messages": [llm_with_tools.invoke([system_msg] + state["messages"])]}
    return result


graph = StateGraph(MessagesState)

graph.add_node("assistant", assistant)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "assistant")
graph.add_conditional_edges(
    "assistant",
    tools_condition,
)
graph.add_edge("tools", "assistant")

app = graph.compile()
