from typing import List, TypedDict
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOpenAI(model_name="gpt-4o")

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState)
graph.add_node("process_node", process)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()

user_input = input("You: ")
while user_input.lower() != "exit":
    state = {"messages": [HumanMessage(content=user_input)]}
    agent.invoke(state)
    user_input = input("You: ")



    


