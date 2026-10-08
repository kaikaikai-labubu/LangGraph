from typing import List, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    values: List[int]
    name: str
    result: str

def process_values(state: AgentState) -> AgentState:
    """This function handles multiple different inputs"""
    print(state)
    state["result"] = f"Hi there {state['name']}! Your sum = {sum(state['values'])}"
    print(state)
    return state

graph = StateGraph(AgentState)
graph.add_node("process_values", process_values)

graph.set_entry_point("process_values")
graph.set_finish_point("process_values")
app = graph.compile()

result = app.invoke({"values": [1, 2, 3], "name": "Kai", "result": ""})
print(result)