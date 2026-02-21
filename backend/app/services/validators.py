import re
from typing import Optional, Tuple, List
from rapidfuzz import fuzz, process


REQUIRED_WARNING = """GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems."""

WARNING_PARA1 = "according to the surgeon general women should not drink alcoholic beverages during pregnancy because of the risk of birth defects"
WARNING_PARA2 = "consumption of alcoholic beverages impairs your ability to drive a car or operate machinery and may cause health problems"

BEVERAGE_TYPES = [
    "bourbon",
    "whiskey",
    "whisky",
    "vodka",
    "gin",
    "rum",
    "tequila",
    "brandy",
    "wine",
    "beer",
    "cordial",
    "liqueur",
    "liquor",
    "cognac",
    "scotch",
    "rye",
    "moonshine",
    "sake",
    "vermouth",
    "absinthe",
]

BEVERAGE_TYPE_VARIANTS = {
    "whiskey": ["whiskey", "whisky", "wiskey", "wisky", "whiskev"],
    "bourbon": ["bourbon", "bourborn", "bourban", "baurbon"],
    "vodka": ["vodka", "vodca", "uodka"],
    "gin": ["gin"],
    "rum": ["rum", "rurn"],
    "tequila": ["tequila", "tequlia", "teguila"],
    "brandy": ["brandy", "brandv", "brandie"],
    "vodka": ["vodka", "vodca"],
    "cognac": ["cognac", "cognac", "cognnac"],
}


def normalize_text(text: str) -> str:
    if not text:
        return ""
    normalized = text.lower()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()


def _fuzzy_contains(text: str, pattern: str, threshold: int = 75) -> bool:
    """Check if pattern is in text using fuzzy matching."""
    if not text or not pattern:
        return False

    text_lower = text.lower()
    pattern_lower = pattern.lower()

    if pattern_lower in text_lower:
        return True

    words = text_lower.split()
    pattern_words = pattern_lower.split()

    if len(pattern_words) == 1:
        for word in words:
            if fuzz.ratio(word, pattern_lower) >= threshold:
                return True
        return False

    for i in range(len(words) - len(pattern_words) + 1):
        segment = " ".join(words[i : i + len(pattern_words)])
        if fuzz.ratio(segment, pattern_lower) >= threshold:
            return True

    return False


def _fuzzy_extract_number(
    text: str, pattern_prefix: str = ""
) -> Tuple[Optional[float], Optional[str]]:
    """Extract number with fuzzy prefix matching."""
    patterns = [
        r"(\d{1,2}(?:\.\d{1,2})?)\s*%",
        r"(\d{2,3})\s*(?:proof)",
        r"(\d{1,2}(?:\.\d{1,2})?)\s*(?:abv|alc)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            return value, match.group(0)

    return None, None


def extract_brand_name(text: str) -> Tuple[Optional[str], float]:
    """Extract brand name - usually prominent text at top of label."""
    if not text:
        return None, 0.0

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return None, 0.0

    best_match = None
    best_conf = 0.0

    full_distillery_pattern = re.compile(
        r"([A-Z]{2,}(?:\s+[A-Z]{2,})+(?:\s+DISTILLING|DISTILLERY)(?:\s+CO\.?)?)",
        re.IGNORECASE,
    )
    for line in lines:
        match = full_distillery_pattern.search(line)
        if match:
            brand = match.group(1).strip()
            brand = re.sub(r"[^\w\s]", "", brand).strip()
            if len(brand.split()) >= 3:
                brand = " ".join(word.capitalize() for word in brand.split())
                return brand, 0.95

    known_brands = [
        (re.compile(r"(RIVER\s*BEND)", re.IGNORECASE), "River Bend"),
        (re.compile(r"(JACK\s*DANIELS?)", re.IGNORECASE), "Jack Daniel's"),
        (re.compile(r"(WILD\s*TURKEY)", re.IGNORECASE), "Wild Turkey"),
        (re.compile(r"(JIM\s*BEAM)", re.IGNORECASE), "Jim Beam"),
        (re.compile(r"(BLUE\s*RIDGE)", re.IGNORECASE), "Blue Ridge"),
        (re.compile(r"(OLD\s*\w+)", re.IGNORECASE), None),
    ]

    for pattern, name in known_brands:
        for line in lines:
            match = pattern.search(line)
            if match:
                if name:
                    return name, 0.9
                else:
                    return match.group(1).strip().title(), 0.85

    distillery_pattern = re.compile(
        r"([A-Z][A-Za-z\s]{2,}(?:DISTILLERY|DISTILLING|BREWERY))", re.IGNORECASE
    )
    for line in lines:
        match = distillery_pattern.search(line)
        if match:
            brand = match.group(1).strip()
            brand = re.sub(r"[^\w\s]", "", brand).strip()
            if len(brand.split()) >= 2 and not best_match:
                brand = " ".join(word.capitalize() for word in brand.split())
                best_match = brand
                best_conf = 0.75

    skip_words = {
        "small",
        "batch",
        "straight",
        "product",
        "usa",
        "aged",
        "years",
        "bottled",
        "distilled",
        "government",
        "warning",
        "according",
        "surgeon",
        "general",
        "women",
        "consumption",
        "alcohol",
        "alc",
        "vol",
        "ml",
        "proof",
        "%",
        "bourbon",
        "whiskey",
        "whisky",
        "vodka",
        "gin",
        "rum",
        "tequila",
        "evansville",
        "indiana",
        "bottled",
        "co",
    }

    for line in lines[:12]:
        words = line.split()
        if len(words) < 2:
            continue

        non_skip_words = [
            w
            for w in words
            if w.lower() not in skip_words
            and not any(c.isdigit() for c in w)
            and len(w) > 2
        ]
        if len(non_skip_words) >= 2:
            cap_words = [w for w in words if w and w[0].isupper()]
            if len(cap_words) >= 2 and not best_match:
                clean_line = re.sub(r"[^\w\s]", "", line).strip()
                clean_line = " ".join(clean_line.split()[:4])
                best_match = clean_line
                best_conf = 0.55

    return best_match, best_conf


def extract_class_type(text: str) -> Tuple[Optional[str], float]:
    """Extract class/type with fuzzy matching for OCR errors."""
    if not text:
        return None, 0.0

    text_lower = text.lower()
    normalized = normalize_text(text)

    small_batch_bourbon = re.search(r"small\s*batch", text_lower)
    if small_batch_bourbon:
        bourbon_nearby = re.search(r"bour.*?(?:whis|iskey|key)", text_lower)
        if bourbon_nearby:
            return "Small Batch Bourbon Whiskey", 0.85
        return "Small Batch", 0.8

    bourbon_whiskey_garbled = re.search(
        r"(?:BOUR|BOARBON|BOURBO)\s*[-\s]*[-\s]*(?:WH?IS?K?E?Y?|ISKEY|HISKEY|KEY)",
        text,
        re.IGNORECASE,
    )
    if bourbon_whiskey_garbled:
        if re.search(r"small\s*batch", text_lower):
            return "Small Batch Bourbon Whiskey", 0.8
        return "Bourbon Whiskey", 0.75

    patterns = [
        (r"(kentucky\s+straight\s+(?:bourbon|whiskey|whisky))", 0.9),
        (r"(straight\s+(?:bourbon|whiskey|whisky|rye))", 0.85),
        (r"(tennessee\s+(?:bourbon|whiskey|whisky))", 0.85),
    ]

    for pattern, conf in patterns:
        match = re.search(pattern, text_lower)
        if match:
            found = match.group(1)
            original_match = re.search(re.escape(found), text, re.IGNORECASE)
            if original_match:
                return original_match.group(0).strip().title(), conf

    for beverage in BEVERAGE_TYPES:
        if beverage in normalized:
            words = normalized.split()
            for i, word in enumerate(words):
                if fuzz.ratio(word, beverage) >= 75:
                    return beverage.title(), 0.7

    return None, 0.0

    text_lower = text.lower()
    normalized = normalize_text(text)

    patterns = [
        (r"(small\s+batch\s+(?:bourbon|whiskey|whisky))", 0.9),
        (r"(kentucky\s+straight\s+(?:bourbon|whiskey|whisky))", 0.9),
        (r"(straight\s+(?:bourbon|whiskey|whisky|rye))", 0.85),
        (r"(tennessee\s+(?:bourbon|whiskey|whisky))", 0.85),
        (r"((?:bourbon|whiskey|whisky)\s+(?:whiskey|whisky))", 0.8),
    ]

    for pattern, conf in patterns:
        match = re.search(pattern, text_lower)
        if match:
            found = match.group(1)
            original_match = re.search(re.escape(found), text, re.IGNORECASE)
            if original_match:
                return original_match.group(0).strip(), conf

    bourbon_whiskey_pattern = re.compile(
        r"(BOUR\s*[-\s]*[BON]*\s*[-\s]*WH?IS?K?E?Y?|BOURBON\s*WH?IS?K?E?Y?|WH?IS?K?E?Y?\s*BOURBON)",
        re.IGNORECASE,
    )
    match = bourbon_whiskey_pattern.search(text)
    if match:
        found = match.group(0).upper()
        if "BOUR" in found and ("WHIS" in found or "KEY" in found or "ISK" in found):
            return "Bourbon Whiskey", 0.8

    for btype, variants in BEVERAGE_TYPE_VARIANTS.items():
        for variant in variants:
            if variant in normalized:
                match = re.search(re.escape(variant), text, re.IGNORECASE)
                if match:
                    return match.group(0).strip().title(), 0.7

    for beverage in BEVERAGE_TYPES:
        words = normalized.split()
        for i, word in enumerate(words):
            if fuzz.ratio(word, beverage) >= 75:
                context_words = words[max(0, i - 2) : min(len(words), i + 3)]
                context = " ".join(context_words)
                original_match = re.search(re.escape(context), text, re.IGNORECASE)
                if original_match:
                    return original_match.group(0).strip(), 0.65

    return None, 0.0

    text_lower = text.lower()
    normalized = normalize_text(text)

    found_types = []

    patterns = [
        (r"(small\s+batch\s+(?:bourbon|whiskey|whisky))", 0.9),
        (r"(kentucky\s+straight\s+(?:bourbon|whiskey|whisky))", 0.9),
        (r"(straight\s+(?:bourbon|whiskey|whisky|rye))", 0.85),
        (r"(tennessee\s+(?:bourbon|whiskey|whisky))", 0.85),
        (r"((?:bourbon|whiskey|whisky)\s+(?:whiskey|whisky))", 0.8),
    ]

    for pattern, conf in patterns:
        match = re.search(pattern, text_lower)
        if match:
            found = match.group(1)
            original_match = re.search(re.escape(found), text, re.IGNORECASE)
            if original_match:
                return original_match.group(0).strip(), conf

    for btype, variants in BEVERAGE_TYPE_VARIANTS.items():
        for variant in variants:
            if variant in normalized:
                match = re.search(re.escape(variant), text, re.IGNORECASE)
                if match:
                    return match.group(0).strip(), 0.7

    for beverage in BEVERAGE_TYPES:
        if beverage in normalized:
            words = normalized.split()
            for i, word in enumerate(words):
                if fuzz.ratio(word, beverage) >= 80:
                    context = " ".join(words[max(0, i - 1) : min(len(words), i + 2)])
                    original_match = re.search(re.escape(context), text, re.IGNORECASE)
                    if original_match:
                        return original_match.group(0).strip(), 0.65

    return None, 0.0


def extract_alcohol_content(text: str) -> Tuple[Optional[str], Optional[float], float]:
    """Extract alcohol content with flexible pattern matching."""
    if not text:
        return None, None, 0.0

    patterns = [
        (r"(\d{1,2}(?:\.\d{1,2})?)\s*%\s*alc\.?\s*/?\s*vol\.?", "abv", 0.95),
        (r"(\d{1,2}(?:\.\d{1,2})?)\s*%\s*(?:abv)", "abv", 0.9),
        (r"(\d{1,2}(?:\.\d{1,2})?)\s*%\s*(?:alcohol)", "abv", 0.9),
        (r"(\d{2,3})\s*(?:proof)", "proof", 0.9),
        (r"(\d{1,2}(?:\.\d{1,2})?)\s*%", "abv_percent", 0.8),
        (r"alc\.?\s*/?\s*vol\.?\s*[:\s]*(\d{1,2}(?:\.\d{1,2})?)", "abv", 0.85),
    ]

    for pattern, ptype, conf in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            original = match.group(0).strip()

            if ptype == "proof":
                abv = value / 2
                return original, abv, conf

            return original, value, conf

    return None, None, 0.0


def extract_net_contents(text: str) -> Tuple[Optional[str], Optional[dict], float]:
    """Extract net contents with fuzzy matching."""
    if not text:
        return None, None, 0.0

    patterns = [
        (r"(\d+(?:\.\d+)?)\s*(ml|mL|ML|milliliter)", "ml", 0.95),
        (r"(\d+(?:\.\d+)?)\s*(l|L|liter|litre)(?!\w)", "l", 0.95),
        (r"(\d+(?:\.\d+)?)\s*(?:fl\.?\s*oz|fluid\s*ounce|oz)", "fl_oz", 0.9),
        (r"(\d+)\s*(mI|ml|mL)", "ml", 0.85),
        (r"(\d+)\s*(l\b|L\b)", "l", 0.85),
    ]

    for pattern, unit_type, conf in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount = float(match.group(1))
            unit = match.group(2).lower()
            original = match.group(0).strip()

            parsed = {"amount": amount, "unit": unit}
            return original, parsed, conf

    return None, None, 0.0


def validate_government_warning(text: str) -> Tuple[Optional[str], List[str], float]:
    """Validate government warning with fuzzy matching for OCR errors."""
    if not text:
        return None, ["No text found"], 0.0

    issues = []
    normalized = normalize_text(text)

    warning_variants = [
        "government warning",
        "govemment warning",
        "goverment warning",
        "governnent warning",
        "governmert warning",
    ]

    header_found = False
    header_all_caps = False

    for variant in warning_variants:
        if variant in normalized:
            header_found = True
            if "GOVERNMENT WARNING" in text or "GOVERNMENT  WARNING" in text:
                header_all_caps = True
            break

    if not header_found:
        for variant in warning_variants:
            if _fuzzy_contains(normalized, variant, threshold=70):
                header_found = True
                break

    if not header_found:
        return None, ["Government Warning not found"], 0.0

    if not header_all_caps:
        issues.append("Header should be 'GOVERNMENT WARNING:' in ALL CAPS")

    para1_keywords = ["surgeon general", "pregnancy", "birth defect"]
    para1_found = (
        sum(1 for kw in para1_keywords if _fuzzy_contains(normalized, kw, 70)) >= 2
    )

    para2_keywords = ["drive", "operate machinery", "health problem", "impair"]
    para2_found = (
        sum(1 for kw in para2_keywords if _fuzzy_contains(normalized, kw, 70)) >= 2
    )

    if not para1_found:
        issues.append("Paragraph (1) content incomplete or missing")
    if not para2_found:
        issues.append("Paragraph (2) content incomplete or missing")

    similarity = fuzz.ratio(normalized, normalize_text(REQUIRED_WARNING)) / 100

    confidence = 0.3
    if header_found:
        confidence += 0.2
    if header_all_caps:
        confidence += 0.15
    if para1_found:
        confidence += 0.175
    if para2_found:
        confidence += 0.175
    confidence = min(confidence + similarity * 0.15, 1.0)

    if issues:
        confidence *= 0.85

    warning_match = re.search(
        r"(government\s*warning\s*:.*?)(?=\n\s*\n|\n\s*[A-Z]{3,}|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    extracted_warning = warning_match.group(0) if warning_match else text[:200]

    return extracted_warning, issues, round(confidence, 2)
