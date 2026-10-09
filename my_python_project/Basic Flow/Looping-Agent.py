from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import random
from pathlib import Path

class AgentState(TypedDict):
    name: str
    number: List[int]
    counter: int

def greeting(state: AgentState) -> AgentState:
    state["name"] = (f"Hello, {state['name']}!")
    state["counter"] = 0
    return state

def random_number(state: AgentState) -> AgentState:
    state["number"].append(random.randint(1, 10))
    state["counter"] += 1
    return state

def should_continue(state: AgentState) -> AgentState:
    if state["counter"] < 5:
        return "loop"
    else:
        return "exit"

graph = StateGraph(AgentState)

graph.add_node("greeting_node", greeting)
graph.add_node("random_number_node", random_number)
graph.add_edge("greeting_node", "random_number_node")

graph.add_conditional_edges("random_number_node", 
    should_continue,
    {
    "loop": "random_number_node",
    "exit": END
})

graph.set_entry_point("greeting_node")

app = graph.compile()

""" image_path = Path(__file__).with_name("conditional-agents-graph.png")
image_path.write_bytes(app.get_graph().draw_mermaid_png())
print(f"Graph image saved to {image_path}") """

print(app.invoke({"name": "Kai", "number": [], "counter": 0}))




