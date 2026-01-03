# AI Research Workflow Demos

This repository contains two different implementations of an AI-powered research workflow that automatically researches topics and generates articles. Each implementation uses a different framework to demonstrate various approaches to building multi-agent AI systems.

## Implementations

### 🤖 [CrewAI Implementation](./crewai/)

A demonstration using **CrewAI**, a framework for orchestrating role-playing autonomous AI agents.

**Key Features:**
- Autonomous agents with specific roles (Researcher, Writer)
- Sequential workflow with agent delegation
- Dual interface: CLI and REST API
- High-level abstractions for agent collaboration

**Best for:** Projects requiring autonomous agent behavior, role-based workflows, and quick setup.

[View CrewAI Demo →](./crewai/README.md)

---

### 📊 [LangGraph Implementation](./langgraph/)

An alternative implementation using **LangGraph**, a library for building stateful, multi-agent applications with explicit graph-based workflows.

**Key Features:**
- Explicit state management using TypedDict
- Graph-based workflow with nodes and edges
- Fine-grained control over execution flow
- Clear visibility into state transitions

**Best for:** Projects needing explicit control, complex branching logic, and detailed workflow visualization.

[View LangGraph Demo →](./langgraph/README.md)

---

## Comparison

| Feature | CrewAI | LangGraph |
|---------|--------|-----------|
| **Abstraction Level** | High-level, agent-focused | Low-level, graph-focused |
| **State Management** | Implicit | Explicit (TypedDict) |
| **Control Flow** | Autonomous agents | Manual graph construction |
| **Learning Curve** | Easier to start | More control, steeper curve |
| **Use Case** | Role-based collaboration | Complex workflows with branching |

## Getting Started

Each implementation has its own directory with:
- Complete setup instructions
- Detailed README
- Independent dependencies
- Working examples

Navigate to either directory and follow the README to get started:

```bash
# Try the CrewAI implementation
cd crewai/
# Follow instructions in crewai/README.md

# Or try the LangGraph implementation
cd langgraph/
# Follow instructions in langgraph/README.md
```

## Requirements

Both implementations require:
- Python 3.11+
- OpenAI API key
- Additional API keys (Serper for CrewAI, Tavily for LangGraph)

## Project Structure

```
.
├── README.md           # This file
├── crewai/            # CrewAI implementation
│   ├── README.md
│   ├── main.py       # CLI interface
│   ├── api.py        # REST API
│   ├── research.py   # Core logic
│   └── pyproject.toml
└── langgraph/        # LangGraph implementation
    ├── README.md
    ├── main.py       # CLI interface
    ├── research.py   # Graph-based workflow
    └── pyproject.toml
```

## Contributing

Feel free to explore both implementations, compare approaches, and experiment with modifications!

## License

MIT
