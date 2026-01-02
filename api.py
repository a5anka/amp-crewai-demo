# api.py - REST API interface for CrewAI research

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from research import run_research

app = FastAPI(
    title="CrewAI Research API",
    description="Generate research articles on any topic using AI agents",
    version="1.0.0"
)


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    article: str


@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "name": "CrewAI Research API",
        "version": "1.0.0",
        "endpoints": {
            "POST /research": "Generate research article on a topic",
            "GET /health": "Health check"
        }
    }


@app.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest):
    """
    Research a topic and generate an article using AI agents

    Args:
        request: ResearchRequest containing the topic to research

    Returns:
        ResearchResponse with the generated article

    Example:
        POST /research
        {"topic": "quantum computing"}
    """
    try:
        if not request.topic or not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")

        result = run_research(request.topic)

        return ResearchResponse(
            topic=request.topic,
            article=result
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "crewai-research"}
