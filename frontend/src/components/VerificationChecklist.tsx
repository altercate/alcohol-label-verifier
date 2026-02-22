"use client";

import { FieldResults, ImageResult } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { FieldCard } from "./FieldCard";

interface VerificationChecklistProps {
  result: ImageResult;
}

const FIELD_LABELS: Record<keyof FieldResults, string> = {
  brand_name: "Brand Name",
  class_type: "Class/Type",
  alcohol_content: "Alcohol Content",
  net_contents: "Net Contents",
  government_warning: "Government Warning",
  bottler_producer: "Bottler/Producer",
  country_of_origin: "Country of Origin",
};

export function VerificationChecklist({ result }: VerificationChecklistProps) {
  const { fields, summary, filename, processing_time_ms } = result;

  return (
    <Card>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div>
            <CardTitle className="text-lg">{filename}</CardTitle>
            <p className="text-sm text-gray-500 mt-1">
              Processed in {processing_time_ms}ms
            </p>
          </div>
          <div className="flex items-center gap-2">
            {summary.is_compliant ? (
              <Badge variant="success">Compliant</Badge>
            ) : (
              <Badge variant="warning">Needs Review</Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-3">
        {(Object.keys(fields) as Array<keyof FieldResults>).map((fieldKey) => (
          <FieldCard
            key={fieldKey}
            label={FIELD_LABELS[fieldKey]}
            result={fields[fieldKey]}
          />
        ))}

        <div className="pt-4 border-t mt-4">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">Summary:</span>
            <div className="flex gap-3">
              <span className="text-green-600">
                {summary.detected} detected
              </span>
              <span className="text-red-600">{summary.missing} missing</span>
              <span className="text-yellow-600">
                {summary.formatting_issues} issues
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
