from fastapi import FastAPI
from shared.contracts.requests.evaluate_match import EvaluateMatchRequest
from shared.contracts.responses.decision_result import DecisionResult
from decision_engine.pipelines.evaluate_match import EvaluateMatchPipeline

app = FastAPI(title="CareerScope Decision Engine")

@app.post("/api/v1/reasoning/evaluate_match", response_model=DecisionResult)
async def evaluate_match_endpoint(request: EvaluateMatchRequest):
    """
    Thin HTTP wrapper around pure deterministic reasoning pipeline.
    """
    return await EvaluateMatchPipeline.execute(request)
