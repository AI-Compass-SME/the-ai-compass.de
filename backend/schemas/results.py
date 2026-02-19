from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class AnalysisResult(BaseModel):
    company_id: int
    response_id: int
    total_score: float
    cluster: Dict[str, Any]
    dimension_scores: Dict[str, float]
    percentiles: Dict[str, float]
    gap_analysis: Dict[str, Any]
    roadmap: Dict[str, Any]
    benchmark_scores: Optional[Dict[str, float]] = None
