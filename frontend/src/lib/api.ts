const API_BASE = process.env.NEXT_PUBLIC_API_URL || '';

export interface FieldResult {
  status: 'detected' | 'missing' | 'formatting_issue';
  value?: string;
  parsed_value?: number | { amount: number; unit: string } | null;
  issues?: string[];
  confidence?: number;
}

export interface FieldResults {
  brand_name: FieldResult;
  class_type: FieldResult;
  alcohol_content: FieldResult;
  net_contents: FieldResult;
  government_warning: FieldResult;
  bottler_producer: FieldResult;
  country_of_origin: FieldResult;
}

export interface Summary {
  detected: number;
  missing: number;
  formatting_issues: number;
  is_compliant: boolean;
}

export interface ImageResult {
  filename: string;
  processing_time_ms: number;
  raw_text?: string;
  fields: FieldResults;
  summary: Summary;
}

export interface BatchSummary {
  total_images: number;
  fully_compliant: number;
  needs_review: number;
}

export interface VerifyResponse {
  results: ImageResult[];
  batch_summary: BatchSummary;
}

export async function verifyLabels(files: File[]): Promise<VerifyResponse> {
  const formData = new FormData();
  
  files.forEach((file) => {
    formData.append('files', file);
  });

  const response = await fetch(`${API_BASE}/api/verify`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}`);
  }

  return response.json();
}
