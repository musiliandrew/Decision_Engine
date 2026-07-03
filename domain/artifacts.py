from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from uuid import UUID

class RequirementAnalysis(BaseModel):
    """Parses and normalizes job requirements into atomic capabilities."""
    job_id: str
    core_requirements: List[str] = Field(default_factory=list)
    secondary_requirements: List[str] = Field(default_factory=list)
    derived_implicit_requirements: List[str] = Field(default_factory=list)

class EvidenceCoverage(BaseModel):
    """Measures how well a capability is backed by objective proof."""
    capability_name: str
    supporting_evidence_ids: List[UUID] = Field(default_factory=list)
    coverage_score: float = Field(default=0.0, ge=0.0, le=100.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class CapabilityAlignment(BaseModel):
    """Maps user capabilities against the RequirementAnalysis."""
    capability_name: str
    is_required: bool
    is_secondary: bool
    alignment_score: float = Field(default=0.0, ge=0.0, le=100.0)
    evidence_coverage: EvidenceCoverage

class GapAnalysis(BaseModel):
    """Identifies missing required capabilities (pure set operations)."""
    missing_core: List[str] = Field(default_factory=list)
    missing_secondary: List[str] = Field(default_factory=list)
    critical_gaps: List[str] = Field(default_factory=list)

class ReadinessAssessment(BaseModel):
    """Aggregates scores into a final mathematical readiness metric."""
    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)
    skill_score: float = Field(default=0.0, ge=0.0, le=100.0)
    evidence_score: float = Field(default=0.0, ge=0.0, le=100.0)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)

class CompanyFitAssessment(BaseModel):
    """Measures cultural and operational alignment."""
    culture_match_score: float = Field(default=0.0, ge=0.0, le=100.0)
    principles_aligned: List[str] = Field(default_factory=list)
    principles_conflicting: List[str] = Field(default_factory=list)

class ExplanationContext(BaseModel):
    """
    The strictly limited context passed to the LLM. 
    The LLM never sees raw data, only these mathematical conclusions.
    """
    overall_readiness: float
    missing_capabilities: List[str]
    strongest_capabilities: List[str]
    confidence: float
    company_fit_score: Optional[float] = None
