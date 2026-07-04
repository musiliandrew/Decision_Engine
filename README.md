# Decision Engine Microservice

A **stateless, pure-inference microservice** designed to evaluate candidate-to-job fit, calculate objective readiness scores, and generate explainable AI reasoning traces. 

Built with **FastAPI** and **`pydantic-ai`**, this service abstracts complex LLM operations (via Google Gemini) into a deterministic, high-throughput HTTP API.

## Architecture Overview
This engine has **zero database dependencies**. It operates purely as a mathematical and reasoning layer. It receives a standardized JSON representation of a Candidate Profile and a Job Description, processes the semantic match, and returns a strict JSON decision payload.

### Core Capabilities
1. **Gap Analysis:** Identifies missing capabilities or skills required for a role.
2. **Win Probability:** Calculates a statistical readiness score based on capability overlap.
3. **Reasoning Traces:** Generates human-readable, explainable AI commentary on why a candidate is or isn't a fit.

## API Contracts

### Endpoint: `/api/v1/reasoning/evaluate_match` (POST)

**Input Example (`EvaluateMatchRequest`)**
```json
{
  "profile_snapshot": {
    "overall_readiness_score": 75.5,
    "strongest_skills": ["Python", "Django", "React"]
  },
  "job_snapshot": {
    "title": "Backend Software Engineer",
    "required_skills": ["Python", "GCP", "SQL"]
  },
  "relevant_evidence": []
}
```

**Output Example (`DecisionResult`)**
```json
{
  "overall_readiness": 82.0,
  "missing_capabilities": ["GCP"],
  "strengths": ["Python", "Backend Software Engineer"],
  "explanations": [
    {
      "conclusion": "Match evaluated for Backend Software Engineer",
      "confidence": 0.85,
      "reasoning_trace": "The candidate has strong Python skills but lacks required GCP knowledge."
    }
  ]
}
```

## Running Locally

1. Create a virtual environment: `python -m venv env`
2. Activate it: `source env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set required API Keys (e.g., `GEMINI_API_KEY`) in your environment.
5. Run the server: `uvicorn api:app --reload --port 8000`
