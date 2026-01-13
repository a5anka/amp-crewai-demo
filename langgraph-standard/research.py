# research.py - Research workflow using LangGraph

import os
from typing import TypedDict, Annotated, Literal
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from tavily import TavilyClient
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode
import operator


# Define the state structure
class ResearchState(TypedDict):
    """State for the research workflow"""
    topic: str
    messages: Annotated[list[BaseMessage], operator.add]
    research_complete: bool
    article: str


# Define Tavily search as a tool
@tool
def tavily_search(query: str) -> str:
    """Search the web for information using Tavily.

    Args:
        query: The search query

    Returns:
        Formatted search results
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    results = client.search(query=query, max_results=5)

    # Format results for the LLM
    formatted_results = []
    for result in results.get("results", []):
        formatted_results.append(
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'N/A')}\n"
        )

    return "\n---\n".join(formatted_results)


def research_agent(state: ResearchState) -> ResearchState:
    """
    Research agent that uses tools to gather information
    """
    # Initialize LLM with tools
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [tavily_search]
    llm_with_tools = llm.bind_tools(tools)

    # Create research prompt if not already in messages
    if len(state["messages"]) == 0:
        system_msg = SystemMessage(
            content="You are a senior research analyst with expertise in uncovering the latest trends and data. "
                    "Use the tavily_search tool to research the topic thoroughly."
        )
        human_msg = HumanMessage(
            content=f"""Research the latest developments in {state['topic']}.

Focus on:
- Key innovations in the last 6 months
- Major players and their contributions
- Emerging trends

Use the search tool to gather information, then provide a detailed bullet-point summary."""
        )
        messages = [system_msg, human_msg]
    else:
        messages = state["messages"]

    # Get response from LLM
    response = llm_with_tools.invoke(messages)

    return {
        **state,
        "messages": [response]
    }


# Should we continue or finish research?
def should_continue_research(state: ResearchState) -> Literal["tools", "write"]:
    """Determine if we should continue research or move to writing"""
    last_message = state["messages"][-1]

    # If the LLM called tools, continue to tool execution
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    # Otherwise, move to writing
    return "write"


def writing_node(state: ResearchState) -> ResearchState:
    """
    Writing node that creates an article based on research
    """
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # Add writing instruction to the conversation
    writing_msg = HumanMessage(
        content=f"""Now write a 3-paragraph article about {state['topic']} that:
- Starts with an engaging hook
- Explains key developments clearly
- Ends with future implications

Target audience: Technical professionals.

Use the research you gathered above to write the article."""
    )

    messages = state["messages"] + [writing_msg]

    # Generate article
    response = llm.invoke(messages)

    return {
        **state,
        "article": response.content,
        "messages": [writing_msg, response]
    }


def create_research_workflow():
    """
    Create and compile the LangGraph research workflow with tool calling
    """
    # Create the graph
    workflow = StateGraph(ResearchState)

    # Create tool node
    tools = [tavily_search]
    tool_node = ToolNode(tools)

    # Add nodes
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("tools", tool_node)
    workflow.add_node("write", writing_node)

    # Add edges
    workflow.set_entry_point("research_agent")

    # Add conditional edge from research agent
    workflow.add_conditional_edges(
        "research_agent",
        should_continue_research,
        {
            "tools": "tools",
            "write": "write"
        }
    )

    # After tools, go back to research agent
    workflow.add_edge("tools", "research_agent")

    # After writing, end
    workflow.add_edge("write", END)

    # Compile the graph
    app = workflow.compile()

    return app


def run_research(topic: str) -> str:
    """
    Run research on a given topic using LangGraph

    Args:
        topic: The topic to research and write about

    Returns:
        str: The generated article
    """
    # Validate required API keys
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY environment variable is not set")

    # Create workflow
    app = create_research_workflow()

    # Initialize state
    initial_state = {
        "topic": topic,
        "messages": [],
        "research_complete": False,
        "article": ""
    }

    # Run the workflow
    result = app.invoke(initial_state)

    return result["article"]


if __name__ == "__main__":
    # Example usage
    topic = "artificial intelligence in healthcare"
    article = run_research(topic)
    print(article)
