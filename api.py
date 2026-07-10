# Touch to reload: Triggering refresh to reload shared/ai/observability.py changes
from fastapi import FastAPI
from shared.contracts.requests.evaluate_match import EvaluateMatchRequest
from shared.contracts.responses.decision_result import DecisionResult
from pipelines.evaluate_match import EvaluateMatchPipeline
from shared.contracts.requests.analyze_rejection import AnalyzeRejectionRequest
from shared.contracts.responses.study_guide import StudyGuideResult
from pipelines.analyze_rejection import AnalyzeRejectionPipeline

app = FastAPI(title="CareerScope Decision Engine")

@app.post("/api/v1/reasoning/evaluate_match", response_model=DecisionResult)
async def evaluate_match_endpoint(request: EvaluateMatchRequest):
    """
    Thin HTTP wrapper around pure deterministic reasoning pipeline.
    """
    return await EvaluateMatchPipeline.execute(request)

@app.post("/api/v1/reasoning/analyze_rejection", response_model=StudyGuideResult)
async def analyze_rejection_endpoint(request: AnalyzeRejectionRequest):
    """
    Synthesizes rejection feedback into a 30-day study guide.
    """
    return await AnalyzeRejectionPipeline.execute(request)
