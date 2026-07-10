from uuid import uuid4
from shared.contracts.requests.analyze_rejection import AnalyzeRejectionRequest
from shared.contracts.responses.study_guide import StudyGuideResult
from shared.ai.providers.gemini import GeminiProvider
from shared.ai.prompts.registry import PromptRegistry
from shared.config.decision import DecisionSettings
from shared.ai.observability import ExecutionContext
import logging

logger = logging.getLogger(__name__)

class AnalyzeRejectionPipeline:
    """
    Synthesizes rejection feedback into an actionable study guide.
    """
    
    @staticmethod
    async def execute(request: AnalyzeRejectionRequest) -> StudyGuideResult:
        settings = DecisionSettings()
        gemini = GeminiProvider(settings)
        prompt = PromptRegistry.load("reasoning.analyze_rejection")
        context = ExecutionContext(trace_id=str(uuid4()))
        
        variables = {
            "company_name": request.company_name,
            "role_title": request.role_title,
            "missing_skills": ", ".join(request.missing_skills) if request.missing_skills else "None specified",
            "extracted_feedback": request.extracted_feedback or "Generic rejection without specific details."
        }
        
        try:
            study_guide = await gemini.generate(
                prompt=prompt,
                response_model=StudyGuideResult,
                context=context,
                variables=variables
            )
            return study_guide
        except Exception as e:
            logger.error(f"Failed to generate study guide: {e}")
            # Fallback
            return StudyGuideResult(
                encouraging_message=f"I saw the update from {request.company_name}. Setbacks happen. Let's pivot and focus on the fundamentals.",
                core_weaknesses=request.missing_skills if request.missing_skills else ["General alignment"],
                action_plan=["Review core requirements for similar roles", "Build a small portfolio project demonstrating these skills"]
            )
