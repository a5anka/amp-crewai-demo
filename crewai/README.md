# CrewAI Research Demo

A demonstration of CrewAI's multi-agent workflow for automated research and content generation. This project uses AI agents to research any topic and generate professional articles.

## Features

- **Multi-agent workflow**: Researcher agent gathers information, Writer agent creates engaging content
- **Dual interface**: Use via command line or REST API
- **Shared logic**: Both CLI and API use the same core research function
- **Clean output**: Formatted blog-style articles

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up API keys:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export SERPER_API_KEY="your-serper-api-key"
# Get Serper key from https://serper.dev
```

## Usage

### CLI (Command Line)

Run the interactive command-line interface:

```bash
uv run python main.py
```

You'll be prompted to enter a topic, and the agents will research and write an article about it.

### REST API

Start the API server:

```bash
uv run uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

#### API Endpoints

- **GET /** - API information
- **GET /health** - Health check
- **POST /research** - Generate research article

#### Example API Usage

```bash
# Using curl
curl -X POST "http://localhost:8000/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing"}'

# Using Python requests
import requests
response = requests.post(
    "http://localhost:8000/research",
    json={"topic": "quantum computing"}
)
print(response.json()["article"])
```

#### API Documentation

Interactive API docs available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
.
├── main.py       # CLI interface
├── api.py        # REST API interface
├── research.py   # Shared research logic
└── pyproject.toml
```

## How It Works

1. **Researcher Agent**: Searches for latest developments, key innovations, and trends
2. **Writer Agent**: Transforms research into a compelling 3-paragraph article
3. **Sequential Process**: Research completes first, then writing begins

## Requirements

- Python >= 3.11
- CrewAI >= 1.7.2
- FastAPI >= 0.115.0 (for API)
- Uvicorn >= 0.32.0 (for API)
- OPENAI_API_KEY environment variable
- SERPER_API_KEY environment variable
