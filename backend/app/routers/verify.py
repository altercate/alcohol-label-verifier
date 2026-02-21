import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

from app.models.schemas import (
    VerifyResponse,
    ImageResult,
    FieldResults,
    FieldResult,
    FieldStatus,
    Summary,
    BatchSummary,
    ErrorResponse,
)
from app.services.ocr import extract_text
from app.services.validators import (
    extract_brand_name,
    extract_class_type,
    extract_alcohol_content,
    extract_net_contents,
    validate_government_warning,
)
from app.config import settings

router = APIRouter()


def process_single_image(file: UploadFile) -> ImageResult:
    start_time = time.time()

    content = file.file.read()

    if len(content) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File {file.filename} exceeds maximum size of {settings.max_file_size_mb}MB",
        )

    try:
        raw_text, ocr_time = extract_text(content)
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"OCR failed for {file.filename}: {str(e)}"
        )

    brand_name_val, brand_conf = extract_brand_name(raw_text)
    class_type_val, class_conf = extract_class_type(raw_text)
    alc_val, alc_parsed, alc_conf = extract_alcohol_content(raw_text)
    net_val, net_parsed, net_conf = extract_net_contents(raw_text)
    warn_val, warn_issues, warn_conf = validate_government_warning(raw_text)

    def make_field_result(
        value, confidence, parsed_value=None, issues=None
    ) -> FieldResult:
        if value is None:
            return FieldResult(status=FieldStatus.MISSING, confidence=confidence)
        elif issues and len(issues) > 0:
            return FieldResult(
                status=FieldStatus.FORMATTING_ISSUE,
                value=value,
                parsed_value=parsed_value,
                issues=issues,
                confidence=confidence,
            )
        else:
            return FieldResult(
                status=FieldStatus.DETECTED,
                value=value,
                parsed_value=parsed_value,
                confidence=confidence,
            )

    brand_result = make_field_result(brand_name_val, brand_conf)
    class_result = make_field_result(class_type_val, class_conf)
    alc_result = make_field_result(alc_val, alc_conf, alc_parsed)
    net_result = make_field_result(net_val, net_conf, net_parsed)
    warn_result = make_field_result(
        warn_val, warn_conf, issues=warn_issues if warn_issues else None
    )

    fields = FieldResults(
        brand_name=brand_result,
        class_type=class_result,
        alcohol_content=alc_result,
        net_contents=net_result,
        government_warning=warn_result,
    )

    detected = sum(
        1
        for f in [brand_result, class_result, alc_result, net_result, warn_result]
        if f.status == FieldStatus.DETECTED
    )
    missing = sum(
        1
        for f in [brand_result, class_result, alc_result, net_result, warn_result]
        if f.status == FieldStatus.MISSING
    )
    formatting_issues = sum(
        1
        for f in [brand_result, class_result, alc_result, net_result, warn_result]
        if f.status == FieldStatus.FORMATTING_ISSUE
    )

    total_time = int((time.time() - start_time) * 1000)

    return ImageResult(
        filename=file.filename or "unknown",
        processing_time_ms=total_time,
        raw_text=raw_text[:1000] if raw_text else None,
        fields=fields,
        summary=Summary(
            detected=detected,
            missing=missing,
            formatting_issues=formatting_issues,
            is_compliant=(missing == 0 and formatting_issues == 0),
        ),
    )


@router.post("/verify", response_model=VerifyResponse)
async def verify_labels(files: List[UploadFile] = File(...)):
    if len(files) > settings.max_files:
        raise HTTPException(
            status_code=400, detail=f"Maximum {settings.max_files} files allowed"
        )

    if len(files) == 0:
        raise HTTPException(status_code=400, detail="At least one file is required")

    results = []
    errors = []

    for file in files:
        try:
            result = process_single_image(file)
            results.append(result)
        except HTTPException as e:
            errors.append({"filename": file.filename, "error": e.detail})
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    if not results and errors:
        raise HTTPException(status_code=422, detail=errors)

    fully_compliant = sum(1 for r in results if r.summary.is_compliant)

    return VerifyResponse(
        results=results,
        batch_summary=BatchSummary(
            total_images=len(results),
            fully_compliant=fully_compliant,
            needs_review=len(results) - fully_compliant,
        ),
    )
