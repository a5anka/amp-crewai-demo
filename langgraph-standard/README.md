# LangGraph Blog Generator

An AI-powered blog article generator built with **LangGraph**, demonstrating stateful, graph-based workflows for automated research and content creation.

## Overview

This application uses LangGraph to orchestrate a multi-step workflow that researches any topic and generates professional blog articles. LangGraph's graph-based approach provides explicit control over workflow state and execution flow, making it ideal for complex, stateful AI applications.

## What is LangGraph?

LangGraph is a library for building stateful, multi-step applications with LLMs using directed graph structures. It enables:

- **Explicit state management** through TypedDict definitions
- **Graph-based workflows** with nodes (functions) and edges (transitions)
- **Fine-grained control** over execution flow and state transitions
- **Easy visualization** of workflow structure and debugging

## How It Works

The application uses a two-node graph workflow:

```
START → Research → Write → END
```

### State Structure

The workflow maintains state using a typed dictionary:

```python
class ResearchState(TypedDict):
    topic: str           # The topic to research
    research_data: str   # Gathered research information
    article: str         # Generated blog article
    messages: list       # Workflow messages
```

### Workflow Nodes

1. **Research Node**:
   - Performs web search using Tavily API
   - Gathers latest information and trends
   - Analyzes key developments
   - Updates state with research findings

2. **Writing Node**:
   - Receives research data from state
   - Generates engaging 3-paragraph article
   - Uses OpenAI to craft compelling content
   - Returns final blog post

### Graph Construction

The workflow is defined as a state graph:

```python
workflow = StateGraph(ResearchState)
workflow.add_node("research", research_node)
workflow.add_node("write", writing_node)
workflow.add_edge(START, "research")
workflow.add_edge("research", "write")
workflow.add_edge("write", END)
```

## Setup

**Note:** Python 3.10 or greater is required.

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set environment variables:
```bash
export OPENAI_API_KEY=your_openai_key
export TAVILY_API_KEY=your_tavily_key
```

Get your API keys:
- OpenAI: https://platform.openai.com/api-keys
- Tavily: https://tavily.com

## Usage

### Command Line Interface

Run the interactive CLI:

```bash
python main.py
```

You'll be prompted to enter a topic, and the system will research and generate a blog article.

### Programmatic Usage

Import and use the research function directly:

```python
from research import run_research

article = run_research("quantum computing")
print(article)
```

## Project Structure

```
.
├── main.py            # CLI interface
├── research.py        # LangGraph workflow definition
├── requirements.txt   # Python dependencies
└── .env.example       # Example environment variables
```

## Key Features

### 1. Explicit State Management
Every piece of data flows through a well-defined state structure, making it easy to track what's happening at each step.

### 2. Graph-Based Architecture
The workflow is defined as a directed graph, providing clear visibility into the execution flow and making it easy to add conditional logic or parallel execution.

### 3. Functional Nodes
Each node is a simple function that takes state and returns updated state, making them easy to test and reason about independently.

### 4. Debugging & Visualization
The graph structure can be easily visualized and debugged, with clear state transitions at each step.

### 5. Flexibility
Adding new nodes, conditional branches, or loops is straightforward thanks to the explicit graph construction.

## Requirements

- Python >= 3.10
- LangGraph >= 0.2.0
- OpenAI API key (for content generation)
- Tavily API key (for web search)

## Use Cases

LangGraph excels in scenarios requiring:

- **Complex workflows** with branching logic and conditionals
- **Stateful applications** where state needs to be tracked and modified across steps
- **Debugging & monitoring** where visibility into state transitions is important
- **Modular design** where workflow steps need to be tested independently
- **Dynamic routing** where execution flow depends on intermediate results

## Extending the Workflow

The graph structure makes it easy to extend:

```python
# Add a new node
workflow.add_node("summarize", summarize_node)

# Add conditional routing
workflow.add_conditional_edges(
    "research",
    should_continue,
    {
        "continue": "write",
        "need_more": "research"
    }
)

# Add parallel execution
workflow.add_node("fact_check", fact_check_node)
workflow.add_edge("research", "fact_check")
```

## License

MIT
