from uuid import uuid4
from shared.contracts.requests.evaluate_match import EvaluateMatchRequest
from shared.contracts.responses.decision_result import DecisionResult, ReasonedExplanation
from shared.domain.features.base import FeatureStore, Feature
from decision_engine.engines.capability_engine import CapabilityEngine

from shared.ai.providers.gemini import GeminiProvider
from shared.ai.prompts.registry import PromptRegistry
from shared.config.decision import DecisionSettings
from shared.ai.observability import ExecutionContext

class EvaluateMatchPipeline:
    """
    Connects the Inference Engine end-to-end.
    """
    
    @staticmethod
    async def execute(request: EvaluateMatchRequest) -> DecisionResult:
        # 1. Feature Extraction (Normally handled by Feature Store upstream, simulated here)
        store = FeatureStore(user_id=uuid4())
        store.features["feat_years_python"] = Feature(id="feat_years_python", value=4.5)
        store.features["feat_github_commits_last_12m"] = Feature(id="feat_github_commits_last_12m", value=312)
        
        # 2. Inference Engine (Belief Generation)
        python_belief = CapabilityEngine.infer_python_capability(store)
        
        # 3. Decision Construction
        is_ready = python_belief.score > 80.0
        overall_score = python_belief.score if is_ready else 0.0
        strengths = [python_belief.capability_id]
        gaps = ["missing_kafka_experience"]
        
        # 4. LLM Explanation Boundary (Synthesizer)
        settings = DecisionSettings()
        gemini = GeminiProvider(settings)
        prompt = PromptRegistry.get("match_score")
        context = ExecutionContext(trace_id=str(uuid4()))
        
        try:
            explanation = await gemini.generate(
                prompt=prompt,
                response_model=ReasonedExplanation,
                context=context,
                variables={
                    "candidate_name": "The Candidate", # Extend IntelligenceSnapshot if you want to pass real names
                    "job_role": request.job_snapshot.title,
                    "score": f"{overall_score:.1f}",
                    "strengths": ", ".join(strengths),
                    "gaps": ", ".join(gaps)
                }
            )
        except Exception as e:
            # Fallback to deterministic stub if LLM fails (e.g. no API key set locally)
            explanation = ReasonedExplanation(
                conclusion=f"Match evaluated for {request.job_snapshot.title}",
                confidence=python_belief.confidence,
                reasoning_trace=f"Computed Score: {python_belief.score} based on {python_belief.evidence_count} evidence streams. (LLM Generation Failed)"
            )
        
        # 5. Return typed Contract
        return DecisionResult(
            overall_readiness=overall_score,
            missing_capabilities=gaps,
            strengths=strengths,
            explanations=[explanation]
        )
