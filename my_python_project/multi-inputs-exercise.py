from typing import List, TypedDict
from langgraph.graph import StateGraph
from functools import reduce

class AgentState(TypedDict):
    values: List[int]
    name: str
    operation: str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    print(state)
    if state["operation"] == "+":
        state["result"] = f"Hi there {state['name']}! Your sum = {sum(state['values'])}"
    elif state["operation"] == "*":
        product = reduce(lambda x, y: x * y, state["values"], 1)
        state["result"] = f"Hi there {state['name']}! Your product = {product}"
    print(state)
    return state

graph = StateGraph(AgentState)
graph.add_node("process_values", process_values)

graph.set_entry_point("process_values")
graph.set_finish_point("process_values")
app = graph.compile()

result = app.invoke({"values": [1, 2, 3, 5], "name": "Kai", "operation": "+"})
print(result)