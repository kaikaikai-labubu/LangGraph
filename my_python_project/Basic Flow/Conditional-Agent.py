from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    finalNumber: int
    operation: str

def add_node(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtract_node(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def router_node(state: AgentState) -> AgentState:
    if state["operation"] == "+":
        return "add_operation"
    elif state["operation"] == "-":
        return "subtract_operation"

graph = StateGraph(AgentState)

graph.add_node("add_operation", add_node)
graph.add_node("subtract_operation", subtract_node)
graph.add_node("router", lambda state: state)

graph.add_edge(START, "router")
graph.add_conditional_edges(
    "router", 
    router_node,
    {
        "add_operation": "add_operation",
        "subtract_operation": "subtract_operation",
    }
)

graph.add_edge("add_operation", END)
graph.add_edge("subtract_operation", END)

app = graph.compile()

inital_state = AgentState(number1=5, number2=3, operation="+")

print(app.invoke(inital_state))

