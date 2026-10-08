from typing import TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    number1: int
    number2: int
    number3: int
    number4: int
    finalNumber: int
    finalNumber2: int
    operation: str
    operation2: str

def addition_operation(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] + state["number2"]
    return state

def subtraction_operation(state: AgentState) -> AgentState:
    state["finalNumber"] = state["number1"] - state["number2"]
    return state

def router1(state: AgentState) -> AgentState:
    if state["operation"] == "+":
        return "addition_operation"
    elif state["operation"] == "-":
        return "subtraction_operation"

def addition_operation2(state: AgentState) -> AgentState:
    state["finalNumber2"] = state["number3"] + state["number4"]
    return state

def subtraction_operation2(state: AgentState) -> AgentState:
    state["finalNumber2"] = state["number3"] - state["number4"]
    return state

def router2(state: AgentState) -> AgentState:
    if state["operation2"] == "+":
        return "addition_operation2"
    elif state["operation2"] == "-":
        return "subtraction_operation2"

graph = StateGraph(AgentState)
graph.add_node("addition_node1", addition_operation)
graph.add_node("subtraction_node1", subtraction_operation)
graph.add_node("router1_node", lambda state: state)

graph.add_node("addition_node2", addition_operation2)
graph.add_node("subtraction_node2", subtraction_operation2)
graph.add_node("router2_node", lambda state: state)


graph.add_edge(START, "router1_node")
graph.add_conditional_edges(
    "router1_node", 
    router1,
    {
        "addition_operation": "addition_node1",
        "subtraction_operation": "subtraction_node1"
})

graph.add_edge("addition_node1", "router2_node")
graph.add_edge("subtraction_node1", "router2_node")

graph.add_conditional_edges(
    "router2_node", 
    router2,
    {
        "addition_operation2": "addition_node2",
        "subtraction_operation2": "subtraction_node2"
    }
)

graph.add_edge("addition_node2", END)
graph.add_edge("subtraction_node2", END)

app = graph.compile()

image_path = Path(__file__).with_name("conditional-agents-graph.png")
image_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph image saved to {image_path}")

initial_state = AgentState(number1 = 10, operation="-", number2 = 5, number3 = 7, number4=2, operation2="+", finalNumber= 0, finalNumber2 = 0)

print(app.invoke(initial_state))