from typing import Dict, TypedDict
from langgraph.graph import StateGraph

class AgentState(TypedDict):
    message: str

def greeting_node(state: AgentState) -> AgentState:
    state["message"] = "Hello!" + state["message"] +"! How you doing?"
    return state

graph = StateGraph(AgentState)
graph.add_node("greeting_node", greeting_node)


graph.set_entry_point("greeting_node")
graph.set_finish_point("greeting_node")
app = graph.compile()

# png_data = app.get_graph().draw_mermaid_png()
# with open("graph.png", "wb") as image_file:
#     image_file.write(png_data)
# print("Graph image saved to graph.png")

result = app.invoke({"message": "Kai"})
print(result)
