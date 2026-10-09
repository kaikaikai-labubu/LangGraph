from typing import List, TypedDict
from langgraph.graph import StateGraph, END
import random
from pathlib import Path

class AgentState(TypedDict):
    player_name: str
    guess: int
    guesses: List[int]
    attempts: int
    lower_bound: int
    upper_bound: int
    answer: int

def setup(state: AgentState) -> AgentState:
    state["attempts"] = 1
    state["lower_bound"] = 1
    state["upper_bound"] = 20
    state["answer"] = random.randint(state["lower_bound"], state["upper_bound"])
    return state

def guess(state: AgentState) -> AgentState:
    state["guess"] = random.randint(state["lower_bound"], state["upper_bound"])
    state["guesses"].append(state["guess"])    
    state["attempts"] += 1
    return state
    

def hint(state: AgentState) -> AgentState:
    if state["guess"] == state["answer"] or state["attempts"] >= 7:
        return "exit"
    elif state["guess"] < state["answer"]:
        print(f"Higher than {state['guess']}")
        state["lower_bound"] = state["guess"]
    else:
        print(f"Lower than {state['guess']}")
        state["upper_bound"] = state["guess"]
    
    return "continue"

graph = StateGraph(AgentState)
graph.add_node("setup_node", setup)
graph.add_node("guess_node", guess)
graph.add_node("hint_node", hint)

graph.add_edge("setup_node", "guess_node")
graph.add_edge("guess_node", "hint_node")
graph.add_conditional_edges("hint_node", 
                           hint, 
                           {"continue": "guess_node", "exit": END})

graph.set_entry_point("setup_node")

app = graph.compile()

# image_path = Path(__file__).with_name("looping-agents-game-graph.png")
# image_path.write_bytes(app.get_graph().draw_mermaid_png())
# print(f"Graph image saved to {image_path}")

initial_state: AgentState = {
    "player_name": "Kai",
    "guess": 0,
    "guesses": [],
    "attempts": 0,
    "lower_bound": 1,
    "upper_bound": 20,
    "answer": 0
}

print(app.invoke(initial_state))



