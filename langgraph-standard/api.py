# api.py - REST API interface for LangGraph research (5-node pipeline)

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from research import run_research

app = FastAPI(
    title="LangGraph Research API",
    description="Generate research articles using 5-node LangGraph pipeline with fact-checking",
    version="2.0.0"
)


class ResearchRequest(BaseModel):
    topic: str


class ResearchResponse(BaseModel):
    topic: str
    article: str
    fact_check_result: str


@app.get("/", response_class=HTMLResponse)
async def home():
    """Home page with input form for demo"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>LangGraph Research Agent</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
            h1 { color: #333; }
            .pipeline { color: #666; font-size: 14px; margin-bottom: 30px; background: #f0f0f0; padding: 10px; border-radius: 4px; }
            .input-section { margin-top: 20px; }
            input[type="text"] { width: 70%; padding: 12px; font-size: 16px; border: 2px solid #ddd; border-radius: 6px; box-sizing: border-box; }
            input[type="text"]:focus { outline: none; border-color: #007bff; }
            button { padding: 12px 30px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 6px; cursor: pointer; margin-left: 10px; }
            button:hover { background: #0056b3; }
            button:disabled { background: #ccc; cursor: not-allowed; }
            .note { margin-top: 15px; color: #888; font-size: 14px; }

            .loading { display: none; margin-top: 30px; text-align: center; }
            .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #007bff; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto 15px; }
            @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            .loading-text { color: #666; }
            .step { color: #888; font-size: 14px; margin-top: 5px; }

            .results { display: none; margin-top: 30px; }
            h2 { color: #555; margin-top: 25px; }
            .article { background: #f8f9fa; padding: 20px; border-radius: 8px; line-height: 1.6; }
            .fact-check { background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; line-height: 1.6; }
            .new-search { margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }
        </style>
    </head>
    <body>
        <h1>LangGraph Research Agent</h1>
        <div class="pipeline">
            <strong>Pipeline:</strong> query_planner → researcher → fact_extractor → writer → fact_checker
        </div>

        <div class="input-section">
            <input type="text" id="topic" placeholder="Enter a topic to research..." autofocus>
            <button id="submit" onclick="doResearch()">Research</button>
            <p class="note">Try: "Claude 4 Opus capabilities" or "LangGraph 2025 features"</p>
        </div>

        <div class="loading" id="loading">
            <div class="spinner"></div>
            <div class="loading-text">Researching...</div>
            <div class="step" id="step">Running pipeline: query_planner → researcher → fact_extractor → writer → fact_checker</div>
        </div>

        <div class="results" id="results">
            <h2>Generated Article</h2>
            <div class="article" id="article"></div>

            <h2>Fact Check Results</h2>
            <div class="fact-check" id="factcheck"></div>

            <div class="new-search">
                <button onclick="resetForm()">New Search</button>
            </div>
        </div>

        <script>
            const steps = [
                "Step 1/5: Planning search queries...",
                "Step 2/5: Executing web searches...",
                "Step 3/5: Extracting facts...",
                "Step 4/5: Writing article...",
                "Step 5/5: Fact checking..."
            ];
            let stepIndex = 0;
            let stepInterval;

            async function doResearch() {
                const topic = document.getElementById('topic').value.trim();
                if (!topic) return;

                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';
                document.getElementById('submit').disabled = true;

                // Animate steps
                stepIndex = 0;
                document.getElementById('step').textContent = steps[0];
                stepInterval = setInterval(() => {
                    if (stepIndex < steps.length - 1) {
                        stepIndex++;
                        document.getElementById('step').textContent = steps[stepIndex];
                    }
                }, 3000);

                try {
                    const response = await fetch('/research', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ topic: topic })
                    });
                    const data = await response.json();

                    // Show results
                    document.getElementById('article').innerHTML = data.article.replace(/\\n/g, '<br>');
                    document.getElementById('factcheck').innerHTML = data.fact_check_result.replace(/\\n/g, '<br>');
                    document.getElementById('results').style.display = 'block';
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    clearInterval(stepInterval);
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('submit').disabled = false;
                }
            }

            function resetForm() {
                document.getElementById('results').style.display = 'none';
                document.getElementById('topic').value = '';
                document.getElementById('topic').focus();
            }

            // Allow Enter key to submit
            document.getElementById('topic').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') doResearch();
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "LangGraph Research API",
        "version": "2.0.0",
        "pipeline": "query_planner → researcher → fact_extractor → writer → fact_checker",
        "endpoints": {
            "GET /": "Home page with input form",
            "POST /research": "Research topic (JSON response)",
            "GET /view?topic=": "Research topic (HTML response)",
            "GET /health": "Health check"
        }
    }


@app.post("/research", response_model=ResearchResponse)
async def research_topic(request: ResearchRequest):
    """
    Research a topic using 5-node pipeline: query_planner → researcher → fact_extractor → writer → fact_checker

    Args:
        request: ResearchRequest containing the topic to research

    Returns:
        ResearchResponse with search queries, extracted facts, article, and fact-check results

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
            article=result["article"],
            fact_check_result=result["fact_check_result"]
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.get("/view", response_class=HTMLResponse)
async def research_view(topic: str):
    """
    Research a topic and view results in browser.

    Open directly in browser: /view?topic=quantum+computing
    """
    try:
        if not topic or not topic.strip():
            raise HTTPException(status_code=400, detail="Topic cannot be empty")

        result = run_research(topic)

        # Convert newlines to HTML breaks
        article_html = result["article"].replace("\n", "<br>")
        fact_check_html = result["fact_check_result"].replace("\n", "<br>")

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Research: {topic}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; line-height: 1.6; }}
                h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
                h2 {{ color: #555; margin-top: 30px; }}
                .article {{ background: #f8f9fa; padding: 20px; border-radius: 8px; }}
                .fact-check {{ background: #fff3cd; padding: 20px; border-radius: 8px; border-left: 4px solid #ffc107; }}
                .pipeline {{ color: #666; font-size: 14px; margin-bottom: 20px; }}
            </style>
        </head>
        <body>
            <h1>Research: {topic}</h1>
            <p class="pipeline">Pipeline: query_planner → researcher → fact_extractor → writer → fact_checker</p>

            <h2>Generated Article</h2>
            <div class="article">{article_html}</div>

            <h2>Fact Check Results</h2>
            <div class="fact-check">{fact_check_html}</div>
        </body>
        </html>
        """
        return HTMLResponse(content=html)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "langgraph-research"}
