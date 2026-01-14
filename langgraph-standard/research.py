# research.py - 5-Node Research Pipeline using LangGraph

import os
from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from tavily import TavilyClient
from langgraph.graph import StateGraph, END
import operator


# Define the state structure
class ResearchState(TypedDict):
    """State for the research workflow"""
    topic: str
    messages: Annotated[list[BaseMessage], operator.add]
    search_queries: list[str]  # Planned search queries from query_planner
    search_results: str  # Raw search results from researcher
    extracted_facts: list[str]  # Facts extracted from research
    article: str  # Generated article
    fact_check_result: str  # Result from fact checker


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
    results = client.search(query=query, max_results=3)

    # Format results for the LLM
    formatted_results = []
    for result in results.get("results", []):
        formatted_results.append(
            f"Title: {result.get('title', 'N/A')}\n"
            f"URL: {result.get('url', 'N/A')}\n"
            f"Content: {result.get('content', 'N/A')}\n"
        )

    return "\n---\n".join(formatted_results)


# ============================================================================
# NODE 1: Query Planner
# ============================================================================
def query_planner(state: ResearchState) -> ResearchState:
    """
    Analyzes the topic and generates strategic search queries.
    This node plans what information to search for.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    system_msg = SystemMessage(
        content="You are a research strategist. Generate 2 focused search queries."
    )

    human_msg = HumanMessage(
        content=f"""Topic: {state['topic']}

Generate exactly 2 specific search queries to research this topic.
Focus on recent developments and technical details.

Return ONLY the queries, one per line, no numbering or bullets."""
    )

    response = llm.invoke([system_msg, human_msg])

    # Parse queries from response
    queries = [q.strip() for q in response.content.strip().split('\n') if q.strip()]

    return {
        **state,
        "search_queries": queries,
        "messages": [system_msg, human_msg, response]
    }


# ============================================================================
# NODE 2: Researcher (Direct Search - No Tool Loop)
# ============================================================================
def researcher(state: ResearchState) -> ResearchState:
    """
    Executes the planned search queries directly using Tavily.
    Simplified approach - no tool calling loop, just direct searches.
    """
    # Get queries (limit to 2 for speed)
    queries = state.get("search_queries", [])[:2]

    # Execute searches directly
    all_results = []
    for query in queries:
        try:
            result = tavily_search.invoke(query)
            all_results.append(f"=== Search: {query} ===\n{result}")
        except Exception as e:
            all_results.append(f"=== Search: {query} ===\nError: {str(e)}")

    search_results = "\n\n".join(all_results)

    # Create message for trace visibility
    research_msg = AIMessage(content=f"Completed {len(queries)} searches.\n\n{search_results}")

    return {
        **state,
        "search_results": search_results,
        "messages": [research_msg]
    }


# ============================================================================
# NODE 3: Fact Extractor
# ============================================================================
def fact_extractor(state: ResearchState) -> ResearchState:
    """
    Extracts key facts from the search results as a structured list.
    This creates a clean fact base that the writer must use.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    # Use the search_results directly
    research_content = state.get("search_results", "")

    system_msg = SystemMessage(
        content="You are a fact extraction specialist. Extract only verifiable facts from research. "
                "Do not add any interpretation or information not explicitly stated in the research."
    )

    human_msg = HumanMessage(
        content=f"""From the search results below, extract key facts as a numbered list.

RULES:
- Only include facts explicitly stated in the search results
- Each fact should be a single, specific claim
- Do NOT add any information not in the search results

Search Results:
{research_content}

Extract 5-8 key facts:"""
    )

    response = llm.invoke([system_msg, human_msg])

    # Parse facts from response
    facts = [line.strip() for line in response.content.strip().split('\n') if line.strip()]

    return {
        **state,
        "extracted_facts": facts,
        "messages": [system_msg, human_msg, response]
    }


# ============================================================================
# NODE 4: Writer
# ============================================================================
def writer(state: ResearchState) -> ResearchState:
    """
    Writes an article using ONLY the extracted facts.
    This is intentionally weak to demonstrate hallucination issues.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    facts_text = "\n".join(state.get("extracted_facts", []))

    system_msg = SystemMessage(
        content="You are a professional tech writer. Write engaging articles based on the facts provided."
    )

    human_msg = HumanMessage(
        content=f"""Write a 3-paragraph article about {state['topic']}.

Available facts:
{facts_text}

Requirements:
- Start with an engaging hook
- Explain key developments clearly
- End with future implications
- Target audience: Technical professionals

Write the article:"""
    )

    response = llm.invoke([system_msg, human_msg])

    return {
        **state,
        "article": response.content,
        "messages": [system_msg, human_msg, response]
    }


# ============================================================================
# NODE 5: Fact Checker
# ============================================================================
def fact_checker(state: ResearchState) -> ResearchState:
    """
    Verifies that claims in the article match the extracted facts.
    Identifies any hallucinated content not supported by research.
    """
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    facts_text = "\n".join(state.get("extracted_facts", []))
    article = state.get("article", "")

    system_msg = SystemMessage(
        content="You are a fact-checking specialist. Compare articles against source facts "
                "and identify any claims not supported by the evidence."
    )

    human_msg = HumanMessage(
        content=f"""Compare the article against the verified facts and identify any issues.

VERIFIED FACTS:
{facts_text}

ARTICLE TO CHECK:
{article}

For each claim in the article, determine if it is:
- VERIFIED: Directly supported by the facts
- UNSUPPORTED: Not found in the facts (potential hallucination)
- EXAGGERATED: Overstates what the facts say

Provide your analysis:"""
    )

    response = llm.invoke([system_msg, human_msg])

    return {
        **state,
        "fact_check_result": response.content,
        "messages": [system_msg, human_msg, response]
    }


def create_research_workflow():
    """
    Create and compile the 5-node LangGraph research workflow.

    Pipeline (linear flow):
    1. query_planner → Plan search strategy
    2. researcher → Execute searches directly
    3. fact_extractor → Extract verified facts
    4. writer → Generate article from facts
    5. fact_checker → Verify article against facts
    """
    # Create the graph
    workflow = StateGraph(ResearchState)

    # Add all 5 nodes
    workflow.add_node("query_planner", query_planner)
    workflow.add_node("researcher", researcher)
    workflow.add_node("fact_extractor", fact_extractor)
    workflow.add_node("writer", writer)
    workflow.add_node("fact_checker", fact_checker)

    # Define linear flow
    workflow.set_entry_point("query_planner")
    workflow.add_edge("query_planner", "researcher")
    workflow.add_edge("researcher", "fact_extractor")
    workflow.add_edge("fact_extractor", "writer")
    workflow.add_edge("writer", "fact_checker")
    workflow.add_edge("fact_checker", END)

    # Compile the graph
    app = workflow.compile()

    return app


def run_research(topic: str) -> dict:
    """
    Run research on a given topic using the 5-node LangGraph pipeline.

    Args:
        topic: The topic to research and write about

    Returns:
        dict: Full result including article, facts, and fact-check results
    """
    # Validate required API keys
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("TAVILY_API_KEY environment variable is not set")

    # Create workflow
    app = create_research_workflow()

    # Initialize state with all required fields
    initial_state = {
        "topic": topic,
        "messages": [],
        "search_queries": [],
        "search_results": "",
        "extracted_facts": [],
        "article": "",
        "fact_check_result": ""
    }

    # Run the workflow
    result = app.invoke(initial_state)

    return {
        "article": result["article"],
        "fact_check_result": result["fact_check_result"]
    }


if __name__ == "__main__":
    # Example usage with 5-node pipeline
    topic = "artificial intelligence in healthcare"
    result = run_research(topic)
    print("Article:", result["article"])
    print("\nFact Check:", result["fact_check_result"])
