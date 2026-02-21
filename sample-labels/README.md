This folder contains sample alcohol label images for testing the verification system.

## Included Sample Labels

| File | Brand | Type | ABV | Volume |
|------|-------|------|-----|--------|
| `river_bend_sample_1.png` | River Bend Distilling Co. | Bourbon Whiskey | 47% Alc./Vol. | 750 mL |
| `pairie_bend_sample_2.png` | Prairie Bend | Whiskey | Varies | 750 mL |
| `mountain_pass_sample_3.png` | Mountain Pass Distilling Co. | Whisky | 55% Alc./Vol. | 750 mL |
| `silver_creek_sample_4.png` | Silver Creek | Spirits | Varies | 750 mL |
| `high_ride_sample_5.png` | High Ride | Bourbon | Varies | 750 mL |

All samples include the full government warning statement.

## Generating Test Labels

Use DALL-E, Midjourney, or Stable Diffusion with prompts like:

**Distilled Spirits:**
> "A realistic alcohol bottle label for 'Old Tom Distillery' Kentucky Straight Bourbon Whiskey, 45% Alc./Vol., 750 mL, with the full government warning text at the bottom, professional product photography, front view"

**Wine:**
> "A realistic wine bottle label for 'Sunset Valley Vineyards' Cabernet Sauvignon, 13.5% Alc. by Vol., 750 mL, with government warning, elegant design, professional photography"

**Craft Spirits:**
> "A realistic craft whiskey label for 'Mountain Pass Distilling Co' Small Batch Whisky, 55% Alc./Vol., 750 mL, with complete government warning statement, rustic design"

## Required Fields for Testing

The system checks for these fields:
- **Brand Name** - Distillery or brand name
- **Class/Type** - Bourbon, Whiskey, Vodka, Gin, Rum, etc.
- **Alcohol Content** - e.g., "45% Alc./Vol." or "90 Proof"
- **Net Contents** - e.g., "750 mL", "1.75 L", "1 L"
- **Government Warning** - Must include "GOVERNMENT WARNING:" in ALL CAPS followed by both paragraphs

## Government Warning Text (Required)

```
GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink alcoholic beverages during pregnancy because of the risk of birth defects. (2) Consumption of alcoholic beverages impairs your ability to drive a car or operate machinery, and may cause health problems.
```

## Tips for Best Results

1. Use high-resolution images (1000px+ height)
2. Ensure good contrast between text and background
3. Avoid glare or shadows on the label
4. Include the complete government warning text
5. Keep text horizontal (not rotated)
