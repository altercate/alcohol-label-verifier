from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel


class FieldStatus(str, Enum):
    DETECTED = "detected"
    MISSING = "missing"
    FORMATTING_ISSUE = "formatting_issue"


class FieldResult(BaseModel):
    status: FieldStatus
    value: Optional[str] = None
    parsed_value: Optional[Any] = None
    issues: Optional[list[str]] = None
    confidence: Optional[float] = None


class FieldResults(BaseModel):
    brand_name: FieldResult
    class_type: FieldResult
    alcohol_content: FieldResult
    net_contents: FieldResult
    government_warning: FieldResult
    bottler_producer: FieldResult
    country_of_origin: FieldResult


class Summary(BaseModel):
    detected: int
    missing: int
    formatting_issues: int
    is_compliant: bool


class ImageResult(BaseModel):
    filename: str
    processing_time_ms: int
    raw_text: Optional[str] = None
    fields: FieldResults
    summary: Summary


class BatchSummary(BaseModel):
    total_images: int
    fully_compliant: int
    needs_review: int


class VerifyResponse(BaseModel):
    results: list[ImageResult]
    batch_summary: BatchSummary


class ErrorResponse(BaseModel):
    code: str
    message: str
    filename: Optional[str] = None
