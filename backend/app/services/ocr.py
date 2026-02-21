import pytesseract
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple, List
import time
import re


def extract_text(image_bytes: bytes, preprocess: bool = True) -> Tuple[str, int]:
    """
    Extract text using fast multi-strategy OCR.
    Target: <5 seconds per image.
    """
    start_time = time.time()

    try:
        pil_image = Image.open(BytesIO(image_bytes))
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
    except Exception:
        return "", int((time.time() - start_time) * 1000)

    results = []

    try:
        text_psm6 = pytesseract.image_to_string(pil_image, lang="eng", config="--psm 6")
        if text_psm6.strip():
            results.append(text_psm6)
    except Exception:
        pass

    try:
        text_psm3 = pytesseract.image_to_string(pil_image, lang="eng", config="--psm 3")
        if text_psm3.strip():
            results.append(text_psm3)
    except Exception:
        pass

    if not results:
        processing_time = int((time.time() - start_time) * 1000)
        return "", processing_time

    combined_text = _combine_results(results)

    processing_time = int((time.time() - start_time) * 1000)

    return combined_text, processing_time


def _combine_results(results: List[str]) -> str:
    """Combine multiple OCR results, keeping the best parts of each."""
    if not results:
        return ""
    if len(results) == 1:
        return results[0]

    combined = results[0]

    for other in results[1:]:
        for line in other.split("\n"):
            line = line.strip()
            if not line:
                continue

            if line not in combined:
                if _is_quality_line(line):
                    combined += "\n" + line

    return combined


def _is_quality_line(line: str) -> bool:
    """Check if a line appears to be quality OCR output."""
    if len(line) < 3:
        return False

    alpha_count = sum(1 for c in line if c.isalpha())
    if alpha_count < len(line) * 0.3:
        return False

    garbage_chars = sum(1 for c in line if c in "|\\/@#$^&*~`[]{}")
    if garbage_chars > len(line) * 0.2:
        return False

    return True


def get_text_with_confidence(image_bytes: bytes) -> Tuple[str, float]:
    """Extract text with confidence score."""
    try:
        pil_image = Image.open(BytesIO(image_bytes))
        if pil_image.mode != "RGB":
            pil_image = Image.convert("RGB")

        data = pytesseract.image_to_data(
            pil_image, output_type=pytesseract.Output.DICT, lang="eng"
        )

        confidences = [int(c) for c in data["conf"] if int(c) > 0]
        avg_confidence = (
            sum(confidences) / len(confidences) / 100 if confidences else 0.5
        )

        text = pytesseract.image_to_string(pil_image, lang="eng", config="--psm 6")

        return text.strip(), round(avg_confidence, 2)

    except Exception as e:
        raise RuntimeError(f"OCR extraction failed: {str(e)}")
