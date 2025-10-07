import os
from typing import Annotated, Literal

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from document.retriever import retriever


class AgentState(dict):
    messages: Annotated[list[BaseMessage], add_messages]


@tool
def get_weather(city: str):
    """Get the weather for a specific city."""
    # This is a placeholder. In a real application, you would call a weather API.
    if "san francisco" in city.lower():
        return "sunny"
    elif "new york" in city.lower():
        return "cloudy"
    else:
        return "I don't know the weather for that city."


def get_graph():
    llm = ChatGroq(temperature=0, model="llama3-70b-8192", api_key=os.environ.get("GROQ_API_KEY"))
    tools = [get_weather]
    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: AgentState):
        user_message = state["messages"][-1].content
        retrieved_chunks = retriever.retrieve(user_message)
        context = "\n".join(retrieved_chunks)
        prompt = f"Context:\n{context}\n\nUser question: {user_message}"
        state["messages"][-1].content = prompt
        return {"messages": [llm_with_tools.invoke(state["messages"])]}

    graph = StateGraph(AgentState)
    graph.add_node("chatbot", chatbot)
    graph.add_node("tools", ToolNode(tools))

    graph.set_entry_point("chatbot")

    def router(state: AgentState) -> Literal["tools", "__end__"]:
        if state["messages"][-1].tool_calls:
            return "tools"
        return END

    graph.add_conditional_edges("chatbot", router)
    graph.add_edge("tools", "chatbot")

    return graph.compile()