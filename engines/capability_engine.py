from typing import List, Dict
from shared.domain.features.base import FeatureStore
from shared.domain.beliefs.base import CapabilityBelief

class CapabilityEngine:
    """
    First deterministic Inference Engine.
    Responsibility: Feature Store -> Belief State
    """
    
    @staticmethod
    def infer_python_capability(feature_store: FeatureStore) -> CapabilityBelief:
        """
        Example mathematical inference algorithm combining factual features into a probabilistic belief.
        """
        # 1. Retrieve Facts (Features)
        years_feature = feature_store.get("feat_years_python")
        commits_feature = feature_store.get("feat_github_commits_last_12m")
        
        years = years_feature.value if years_feature else 0.0
        commits = commits_feature.value if commits_feature else 0
        
        # 2. Mathematical Inference
        score = min(100.0, (years * 10) + (commits * 0.1))
        
        # 3. Calculate Uncertainty
        evidence_count = 0
        if years_feature: evidence_count += 1
        if commits_feature: evidence_count += 1
        
        confidence = 0.0
        if evidence_count > 0:
            confidence = 0.4 + (0.3 * (evidence_count / 2.0))
        if commits > 100:
            confidence = min(0.95, confidence + 0.2)
            
        # 4. Construct the new Belief
        return CapabilityBelief(
            capability_id="cap_python_engineering",
            score=score,
            confidence=confidence,
            uncertainty=1.0 - confidence,
            evidence_count=evidence_count,
            freshness=1.0 if commits > 0 else 0.5,
            stability=0.8 # Mock
        )
