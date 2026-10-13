from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, MessagesState, StateGraph
from typing import List, Sequence
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Annotated, TypedDict

load_dotenv()

llm = ChatOpenAI(model = "gpt-4o")

generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a professional LinkedIn content assistant tasked with crafting engaging, insightful, and well-structured LinkedIn posts."
            " Generate the best LinkedIn post possible for the user's request."
            " If the user provides feedback or critique, respond with a refined version of your previous attempts, improving clarity, tone, or engagement as needed.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

generate_chain = generation_prompt | llm

reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a professional LinkedIn content strategist and thought leadership expert. Your task is to critically evaluate the given LinkedIn post and provide a comprehensive critique. Follow these guidelines:

        1. Assess the post’s overall quality, professionalism, and alignment with LinkedIn best practices.
        2. Evaluate the structure, tone, clarity, and readability of the post.
        3. Analyze the post’s potential for engagement (likes, comments, shares) and its effectiveness in building professional credibility.
        4. Consider the post’s relevance to the author’s industry, audience, or current trends.
        5. Examine the use of formatting (e.g., line breaks, bullet points), hashtags, mentions, and media (if any).
        6. Evaluate the effectiveness of any call-to-action or takeaway.

        Provide a detailed critique that includes:
        - A brief explanation of the post’s strengths and weaknesses.
        - Specific areas that could be improved.
        - Actionable suggestions for enhancing clarity, engagement, and professionalism.

        Your critique will be used to improve the post in the next revision step, so ensure your feedback is thoughtful, constructive, and practical.
        """
    ),
    MessagesPlaceholder(variable_name="messages")
])

reflect_chain = reflection_prompt | llm

graph = StateGraph(MessagesState)

def generation_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
    generated_post = generate_chain.invoke({"messages": state["messages"]})
    return {"messages": [AIMessage(content=generated_post.content)]}

def reflection_node(state: MessagesState) -> dict[str, list[BaseMessage]]:
    res = reflect_chain.invoke({"messages": state["messages"]})
    return {"messages": [HumanMessage(content=res.content)]}

graph.add_node("generate", generation_node)
graph.add_node("reflect", reflection_node)

graph.set_entry_point("generate")

graph.add_edge("reflect", "generate")

def should_continue(state: MessagesState):
    print(state["messages"])
    print(len(state["messages"]))
    print("----------------------------------------------------------------------")
    if len(state["messages"]) > 6:
        return END
    return "reflect"

graph.add_conditional_edges(
    "generate",
    should_continue,
    {END: END, "reflect": "reflect"},
)

workflow = graph.compile()

inputs = {"messages": [HumanMessage(content="""Write a linkedin post on getting a software developer job at IBM under 160 characters""")]}

response = workflow.invoke(inputs)

response["messages"][1].content

response["messages"][2].content

print(workflow.get_graph().draw_mermaid())