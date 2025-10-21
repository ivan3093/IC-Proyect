from pydantic import BaseModel
from typing import Dict, List, Optional


###MODELS###

#using None as a datatype so the user doesnt have to input both userID and email
class UserValidationRequest(BaseModel):
    userId: Optional[str] = None
    email: Optional[str] = None

#defines the body to generate tokens
class TokenRequest(BaseModel):
    client_id: str
    client_secret: str

#Basic Model for HelloResponse Primarly for testing
class HelloResponse(BaseModel):
    message: str
    timestamp: str
    success: bool


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
    chart_url_png: str # <--- nuevo


class AnalysisError(BaseModel):
    error_type: str
    message: str
    failed_line_number: Optional[int] = None
    failed_line_content: Optional[str] = None
    last_success_line_number: Optional[int] = None
    last_success_line_content: Optional[str] = None


