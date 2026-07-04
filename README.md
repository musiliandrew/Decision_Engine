# CareerScoper Decision Engine

The Decision Engine is a **stateless, pure-inference microservice** for the CareerScoper ecosystem. It evaluates candidate-to-job fit, calculates objective readiness scores, and generates explainable reasoning traces using Google Gemini.

It is built with **FastAPI** and **`pydantic-ai`**.

## Architecture Overview
Unlike standard web applications, the Decision Engine has **zero database dependencies**. It does not connect to Postgres, Redis, or any Vector DB. It operates purely as a mathematical inference engine. 

It receives a standardized JSON representation of a Candidate Profile and a Job Description, runs a deterministic pipeline alongside a Gemini reasoning layer, and returns a strict JSON response.

### How it integrates with CareerScoper
1. **The Monolith (Django):** The main CareerScoper API queries the database to gather a user's skills and the specific job details.
2. **The Hand-off:** Django formats this data into an `EvaluateMatchRequest` and sends it to the Decision Engine via an HTTP POST request.
3. **Inference:** The Decision Engine processes the match, checking for capability gaps, calculating a win probability, and using Gemini to generate a human-readable explanation (`ReasonedExplanation`).
4. **The Return:** The engine returns a `DecisionResult` JSON payload back to Django.
5. **Storage:** Django receives the result and caches it in the shared Postgres database (`JobMatchScores` table) so the engine doesn't need to recalculate it again.

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
4. Run the server: `uvicorn api:app --reload --port 8000`

Ensure you have your Google Cloud credentials/API keys configured in your environment to allow Gemini to execute.
