from pydantic import BaseModel
from typing import Dict, List, Optional


class Metrics(BaseModel):
    counts: Dict[str, int]
    percent: Dict[str, float]
    top: dict | None = None
    duration_ms: int = 0


class AnalysisSuccess(BaseModel):
    source_filename: str
    result: Dict[str, List[str]]
    metrics: Metrics
    report_url_html: str


class AnalysisError(BaseModel):
    error_type: str
    message: str
    failed_line_number: Optional[int] = None
    failed_line_content: Optional[str] = None
    last_success_line_number: Optional[int] = None
    last_success_line_content: Optional[str] = None
