This folder contains sample alcohol label images for testing the verification system.

## Included Sample Labels

| File | Brand | Type | ABV | Volume |
|------|-------|------|-----|--------|
| `river_bend_sample_1.png` | River Bend Distilling Co. | Bourbon Whiskey | 47% Alc./Vol. | 750 mL |
| `pairie_bend_sample_2.png` | Prairie Bend Distilling Co. | Straight Rye Whiskey | 50% Alc./Vol. | 750 mL |
| `mountain_pass_sample_3.png` | Mountain Pass Distilling Co. | Whisky | 55% Alc./Vol. | 750 mL |
| `silver_creek_sample_4.png` | Silver Creek Distilling Co. | Whiskey | 48% Alc./Vol. | 750 mL |
| `high_ride_sample_5.png` | High Ridge Distilling | Single Barrel Bourbon | 53% Alc./Vol. | 750 mL |

All samples include the full government warning statement as required by 27 CFR § 16.21.

## TTB Label Requirements

The system checks for these required fields per TTB regulations:

### Brand Name
- Must appear on the label
- Should match the name on the basic permit
- Reference: 27 CFR 5.66

### Class/Type Designation
- Must identify the specific type of spirits (e.g., Bourbon, Vodka, Gin)
- Common types: Bourbon, Whiskey, Whisky, Vodka, Gin, Rum, Tequila, Brandy
- Reference: 27 CFR 5.51

### Alcohol Content
- Expressed as percentage of alcohol by volume
- Acceptable formats: "45% Alc. by Vol.", "45% Alc./Vol.", "ALCOHOL 45% BY VOLUME"
- Note: "ABV" abbreviation is NOT allowed per TTB regulations
- Proof statements (e.g., "90 Proof") may also appear
- Reference: 27 CFR 5.63

### Net Contents
- Standard sizes: 50 mL, 200 mL, 375 mL, 750 mL, 1 L, 1.75 L
- Must appear in metric units
- Reference: 27 CFR 5.47

### Government Warning
Required exact text per 27 CFR § 16.21:

```
GOVERNMENT WARNING: (1) According to the Surgeon General, women should not drink 
alcoholic beverages during pregnancy because of the risk of birth defects. 
(2) Consumption of alcoholic beverages impairs your ability to drive a car or 
operate machinery, and may cause health problems.
```

**Important:** The header "GOVERNMENT WARNING:" must appear in ALL CAPS.

## Generating Test Labels

Use DALL-E, Midjourney, or Stable Diffusion with prompts like:

**Distilled Spirits:**
> "A realistic alcohol bottle label for 'Old Tom Distillery' Kentucky Straight Bourbon Whiskey, 45% Alc./Vol., 750 mL, with the full government warning text at the bottom, professional product photography, front view"

**Wine:**
> "A realistic wine bottle label for 'Sunset Valley Vineyards' Cabernet Sauvignon, 13.5% Alc. by Vol., 750 mL, with government warning, elegant design, professional photography"

**Craft Spirits:**
> "A realistic craft whiskey label for 'Mountain Pass Distilling Co' Small Batch Whisky, 55% Alc./Vol., 750 mL, with complete government warning statement, rustic design"

## Tips for Best Results

1. Use high-resolution images (1000px+ height)
2. Ensure good contrast between text and background
3. Avoid glare or shadows on the label
4. Include the complete government warning text
5. Keep text horizontal (not rotated)
6. Use "Alc./Vol." format (not "ABV") for TTB compliance

## References

- [TTB Labeling Regulations](https://www.ttb.gov/labeling)
- [27 CFR Part 5 - Labeling and Advertising of Distilled Spirits](https://www.ecfr.gov/current/title-27/chapter-I/subchapter-A/part-5)
- [Government Warning Requirements](https://www.ttb.gov/labeling/government-warning)
