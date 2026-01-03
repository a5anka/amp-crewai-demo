# LangGraph Research Demo

This is a research workflow implementation using **LangGraph**, providing an alternative to the CrewAI implementation in the `crewai/` folder.

## Overview

LangGraph is a library for building stateful, multi-agent applications with LLMs using graph-based workflows. This implementation recreates the same research workflow as the CrewAI version but using LangGraph's state-based approach.

## Key Differences from CrewAI

### Architecture
- **CrewAI**: Uses autonomous agents with roles and delegation
- **LangGraph**: Uses explicit state management with nodes and edges in a graph

### Workflow Definition
- **CrewAI**: Sequential process with Agent → Task assignments
- **LangGraph**: Explicit graph with nodes (functions) and edges (transitions)

### State Management
- **CrewAI**: Implicit state passing between agents
- **LangGraph**: Explicit state using TypedDict, tracked through the graph

### Control Flow
- **CrewAI**: Process.sequential handles orchestration
- **LangGraph**: Manual graph construction with `add_node()` and `add_edge()`

## Implementation Details

### State Structure
```python
class ResearchState(TypedDict):
    topic: str
    research_data: str
    article: str
    messages: Annotated[list, operator.add]
```

### Graph Nodes
1. **research_node**: Performs web search and analysis
2. **writing_node**: Generates article from research data

### Workflow
```
START → research → write → END
```

## Setup

1. Install dependencies:
```bash
uv pip install -e .
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_openai_key
export TAVILY_API_KEY=your_tavily_key
```

## Usage

### CLI
```bash
python main.py
```

### Programmatic
```python
from research import run_research

article = run_research("artificial intelligence in healthcare")
print(article)
```

## Requirements

- Python 3.11+
- OpenAI API key (for LLM)
- Tavily API key (for search)

## Advantages of LangGraph

1. **Explicit Control**: Fine-grained control over workflow execution
2. **State Visibility**: Clear state structure and transitions
3. **Flexibility**: Easy to add conditional logic, loops, or parallel execution
4. **Debugging**: Better visibility into state at each step
5. **Modularity**: Nodes are simple functions that can be tested independently

## When to Use LangGraph vs CrewAI

**Use LangGraph when:**
- You need explicit control over workflow state
- Your workflow has complex branching or conditional logic
- You want to easily visualize and debug the workflow graph
- You prefer functional programming patterns

**Use CrewAI when:**
- You want autonomous agent behavior
- You need agent delegation and collaboration
- You prefer a higher-level abstraction
- Your workflow maps well to human-like roles and tasks
