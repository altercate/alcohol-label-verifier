# AI-Powered Alcohol Label Verification App

A proof-of-concept web application that uses OCR to verify alcohol label compliance by detecting required fields.

> **Note:** This is a prototype, not a production compliance system. See [Limitations](#limitations) and [Trade-offs](#ocr-trade-offs) for details.

## How It Works

1. **Upload** - Drag and drop label images (up to 10 at once)
2. **OCR Extraction** - Tesseract extracts text using multiple recognition strategies
3. **Field Detection** - Validators with fuzzy matching detect required fields despite OCR errors
4. **Results** - Clear checklist showing detected, missing, and formatting issues

## Features

- Upload one or multiple label images (up to 10)
- OCR text extraction using Tesseract
- Automatic detection of required fields:
  - Brand Name
  - Class/Type designation
  - Alcohol Content (e.g., 45% Alc./Vol.)
  - Net Contents (e.g., 750 mL)
  - Government Warning (with exact text validation)
- Clear checklist UI showing detected, missing, and formatting issues
- Response time under 5 seconds per image

## Tech Stack

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS, shadcn/ui components
- **Backend**: FastAPI (Python 3.11+), Pydantic
- **OCR**: Tesseract 5.x with multi-PSM strategy
- **Image Processing**: OpenCV, Pillow (available but not used in fast mode)
- **Fuzzy Matching**: RapidFuzz for tolerant text comparison
- **Deployment**: Vercel (frontend) + Render (backend)

## Prerequisites

- Node.js 18+
- Python 3.11+
- Tesseract OCR

### Installing Tesseract

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**Windows:**
Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)

## Quick Start

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## API Reference

### POST /api/verify

Upload label images for verification.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `files[]` - Array of image files (max 10)

**Response:**
```json
{
  "results": [
    {
      "filename": "label.jpg",
      "processing_time_ms": 2847,
      "raw_text": "extracted text...",
      "fields": {
        "brand_name": { "status": "detected", "value": "Brand Name", "confidence": 0.85 },
        "class_type": { "status": "detected", "value": "Bourbon", "confidence": 0.90 },
        "alcohol_content": { "status": "detected", "value": "45% Alc./Vol.", "parsed_value": 45.0, "confidence": 0.95 },
        "net_contents": { "status": "detected", "value": "750 mL", "confidence": 0.92 },
        "government_warning": { "status": "formatting_issue", "issues": ["Header not in ALL CAPS"], "confidence": 0.70 }
      },
      "summary": {
        "detected": 4,
        "missing": 0,
        "formatting_issues": 1,
        "is_compliant": false
      }
    }
  ],
  "batch_summary": {
    "total_images": 1,
    "fully_compliant": 0,
    "needs_review": 1
  }
}
```

## Project Structure

```
alcohol-label-verifier/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── config.py            # Configuration settings
│   │   ├── routers/
│   │   │   └── verify.py        # /api/verify endpoint
│   │   ├── services/
│   │   │   ├── ocr.py           # Tesseract wrapper
│   │   │   ├── preprocessor.py  # Image enhancement
│   │   │   └── validators.py    # Field extraction logic
│   │   └── models/
│   │       └── schemas.py       # Pydantic models
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx         # Main page
│   │   │   └── globals.css
│   │   ├── components/
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── VerificationChecklist.tsx
│   │   │   ├── FieldCard.tsx
│   │   │   ├── BatchResults.tsx
│   │   │   └── ui/              # shadcn-style components
│   │   └── lib/
│   │       ├── api.ts           # API client
│   │       └── utils.ts         # Utilities
│   ├── package.json
│   └── next.config.js
│
└── README.md
```

## Deployment

### Backend (Render)

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `TESSERACT_CMD=/usr/bin/tesseract`

### Frontend (Vercel)

1. Import project from GitHub
2. Set root directory to `frontend`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`

## Approach

### Design Decisions

This prototype was built with the following constraints and goals:

1. **No External API Calls** - Per IT requirements, the system must work without cloud API dependencies. Tesseract was chosen over Google Vision/AWS Textract for offline capability.

2. **<5 Second Response Time** - The previous scanning vendor pilot failed because of 30-40 second processing times. Speed was prioritized over maximum accuracy.

3. **Simple UI** - Designed for users with varying technical comfort levels. Large upload area, clear status indicators, no hidden menus.

4. **Fuzzy Matching** - OCR output is imperfect. Validators tolerate common OCR errors while still catching compliance issues.

5. **Standalone Prototype** - No integration with COLA system, designed to be evaluated independently.

### Tools Used

| Category | Tool | Reason |
|----------|------|--------|
| Frontend Framework | Next.js 14 | Fast development, good DX, easy Vercel deployment |
| UI Components | shadcn/ui | Accessible, clean design, customizable |
| Backend Framework | FastAPI | Async support, automatic OpenAPI docs, Pydantic validation |
| OCR Engine | Tesseract 5.x | Free, local, no API limits |
| Fuzzy Matching | RapidFuzz | Fast string similarity for OCR error tolerance |
| Image Processing | OpenCV, Pillow | Available for preprocessing (not used in fast mode) |

## OCR Approach

### Initial Implementation: Heavy Preprocessing

The first OCR implementation used extensive image preprocessing:
- OpenCV-based image enhancement (CLAHE, denoising, thresholding)
- Multiple preprocessing modes (standard, high-contrast, upscale, adaptive, aggressive)
- Multiple Tesseract PSM modes (3, 4, 6, 11, 12)
- Result quality scoring to select best output

**Problem:** Processing time was 15-57 seconds per image, far exceeding the 5-second requirement.

### Final Implementation: Multi-Strategy Raw OCR

The optimized approach:
- Runs Tesseract with PSM 6 (uniform block of text) and PSM 3 (auto-detection)
- Combines results from both passes, keeping quality lines
- No image preprocessing (uses raw images)
- Smart validators with fuzzy matching for OCR errors

**Result:** Processing time reduced to 3-5 seconds per image.

### OCR Trade-offs

| Trade-off | What We Gained | What We Lost |
|-----------|----------------|--------------|
| **No preprocessing** | ~10x faster processing, simpler code | Lower accuracy on low-quality/angled images |
| **Multi-PSM strategy** | Better coverage of different label layouts | Slightly more CPU usage (2 OCR passes) |
| **Fuzzy field matching** | Handles OCR typos ("BOUR ISKEY" → Bourbon Whiskey) | May accept slightly incorrect values |
| **Known brand patterns** | High accuracy for common distilleries | May miss unknown brand names |
| **Local Tesseract** | No API costs, works offline, no rate limits | Lower accuracy than cloud OCR (Google Vision, AWS Textract) |

## Limitations

### OCR Limitations

1. **Image Quality Dependent**
   - Realistic label images with textures, gradients, or decorative fonts challenge Tesseract
   - Glare, shadows, and low contrast significantly reduce accuracy
   - Angled or rotated images may fail completely

2. **Brand Name Detection**
   - Uses pattern matching for known distilleries
   - Unknown brands rely on heuristics (capitalization, position)
   - May extract incorrect text for unfamiliar labels

3. **Government Warning Validation**
   - Uses fuzzy matching (tolerates OCR errors)
   - May accept warnings with minor text differences
   - Doesn't verify exact font size or positioning requirements

4. **No Image Preprocessing**
   - Earlier version with preprocessing was too slow (15-57s)
   - Current version trades accuracy for speed
   - Users may need to provide high-quality images

### System Limitations

- **No authentication** - Anyone can access the API
- **No persistent storage** - Results not saved between sessions
- **Sequential batch processing** - Images processed one at a time
- **No PDF support** - Only image files accepted
- **English only** - Tesseract configured for English text only

### Not Production-Ready

This is a proof-of-concept with intentional simplifications:
- No integration with TTB COLA system
- No compliance rules engine
- No audit logging
- No user management
- No rate limiting

## Future Improvements

If this were to become a production system:

1. **Upgrade OCR**
   - Consider Google Vision API or AWS Textract for better accuracy
   - Add image preprocessing as optional "enhanced mode" for difficult images
   - Implement image quality checks before processing

2. **Better Brand Detection**
   - Train a small ML model on TTB label database
   - Use NER (Named Entity Recognition) for brand extraction
   - Build a database of known brands for exact matching

3. **Compliance Rules**
   - Implement full TTB label requirements (varies by beverage type)
   - Add validation for font sizes, positioning
   - Support for wine vs spirits vs beer requirements

4. **Batch Processing**
   - Parallel image processing with asyncio
   - Progress tracking for large batches
   - Result caching for duplicate images

5. **Integration**
   - Connect to COLA system for application matching
   - Export results to compliance workflow
   - Add audit trail and compliance reporting

## Assumptions Made

1. **Users provide reasonable quality images** - The system works best with clear, well-lit photos
2. **Labels are in English** - Tesseract configured for English only
3. **Standard label formats** - Validators tuned for typical US alcohol label layouts
4. **Single beverage type per image** - No mixed-type labels
5. **Compliance agents will review results** - This is a verification aid, not autonomous approval

## Performance

| Image Type | Processing Time | Accuracy |
|------------|-----------------|----------|
| Simple text (generated) | ~700ms | 5/5 fields |
| Realistic label (AI-generated) | ~4.5s | 5/5 fields |
| Low quality/angled | ~5s | 3-4/5 fields |

The system meets the <5 second requirement for most images.

## Testing with Sample Labels

You can generate test labels using AI image tools like:
- DALL-E
- Midjourney
- Stable Diffusion

Example prompt:
> "A realistic alcohol bottle label for 'Old Tom Distillery' Kentucky Straight Bourbon Whiskey, 45% Alc./Vol., 750 mL, with the full government warning text at the bottom, professional product photography"

## License

MIT
