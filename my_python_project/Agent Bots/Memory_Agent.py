from langgraph.graph import END, START, StateGraph
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import List, TypedDict, Union

load_dotenv()

class MemoryAgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

llm = ChatOpenAI(model_name="gpt-4o")

def process(state: MemoryAgentState) -> MemoryAgentState:    
    response = llm.invoke(state["messages"])
    state["messages"].append(AIMessage(content=response.content))    
    print(f"\nAI: {response.content}")
    print(f"\nConversation history: {state['messages']}")
    return state

graph = StateGraph(MemoryAgentState)
graph.add_node("process_node", process)
graph.add_edge(START, "process_node")
graph.add_edge("process_node", END)

agent = graph.compile()

conversation_history = []

user_input = input("You: ")
while user_input.lower() != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    state = {"messages": conversation_history}
    result = agent.invoke(state)
    conversation_history = result["messages"]
    user_input = input("You: ")



