from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int) -> int:
    """Adds two integers together."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

tools = [add, multiply]

model = ChatOpenAI(model = "gpt-4o").bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI assistant, please answer the following based on the current state:")
    response = model.invoke([system_prompt] + state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("agent_node", model_call)
tool_node = ToolNode(tools=tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("agent_node")
graph.add_edge("tools", "agent_node")

graph.add_conditional_edges(
    "agent_node",
    should_continue,
    {"end": END, "continue": "tools"}
)

app = graph.compile()

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("Add 40 + 12 and then multiply the result by 2.")]}
print_stream(app.stream(inputs, stream_mode="values"))








