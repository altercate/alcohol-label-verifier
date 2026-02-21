import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from typing import Optional, Tuple


def preprocess_for_ocr(
    image_bytes: bytes, mode: str = "standard"
) -> Tuple[bytes, dict]:
    """
    Multiple preprocessing modes for different label styles.
    Returns processed image bytes and metadata about processing.
    """
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            pil_img = Image.open(BytesIO(image_bytes))
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape

        metadata = {"original_size": (width, height), "mode": mode}

        if mode == "standard":
            processed = _standard_preprocess(gray)
        elif mode == "high_contrast":
            processed = _high_contrast_preprocess(gray)
        elif mode == "upscale":
            processed = _upscale_preprocess(gray)
        elif mode == "adaptive":
            processed = _adaptive_preprocess(gray)
        elif mode == "aggressive":
            processed = _aggressive_preprocess(gray)
        else:
            processed = _standard_preprocess(gray)

        metadata["processed_size"] = processed.shape[::-1]

        pil_processed = Image.fromarray(processed)
        output_buffer = BytesIO()
        pil_processed.save(output_buffer, format="PNG")

        return output_buffer.getvalue(), metadata

    except Exception as e:
        return image_bytes, {"error": str(e)}


def _standard_preprocess(gray: np.ndarray) -> np.ndarray:
    height, width = gray.shape
    if max(height, width) < 2000:
        scale = 2000 / max(height, width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary


def _high_contrast_preprocess(gray: np.ndarray) -> np.ndarray:
    height, width = gray.shape
    if max(height, width) < 2500:
        scale = 2500 / max(height, width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    clahe = cv2.createCLAHE(clipLimit=4.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((2, 2), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary


def _upscale_preprocess(gray: np.ndarray) -> np.ndarray:
    height, width = gray.shape
    if max(height, width) < 3000:
        scale = 3000 / max(height, width)
        gray = cv2.resize(
            gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4
        )

    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return binary


def _adaptive_preprocess(gray: np.ndarray) -> np.ndarray:
    height, width = gray.shape
    if max(height, width) < 2000:
        scale = 2000 / max(height, width)
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    return binary


def _aggressive_preprocess(gray: np.ndarray) -> np.ndarray:
    height, width = gray.shape
    scale = 3000 / max(height, width) if max(height, width) < 3000 else 1.0
    if scale > 1:
        gray = cv2.resize(
            gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4
        )

    denoised = cv2.fastNlMeansDenoising(gray, None, 15, 7, 21)

    clahe = cv2.createCLAHE(clipLimit=5.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(denoised)

    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = np.ones((1, 1), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return binary


def preprocess_image(image_bytes: bytes, enhance_level: str = "medium") -> bytes:
    """Legacy function for backward compatibility."""
    result, _ = preprocess_for_ocr(image_bytes, "standard")
    return result


def get_image_info(image_bytes: bytes) -> Optional[dict]:
    try:
        img = Image.open(BytesIO(image_bytes))
        return {"format": img.format, "size": img.size, "mode": img.mode}
    except Exception:
        return None
