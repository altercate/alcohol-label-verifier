"use client";

import { VerifyResponse } from "@/lib/api";
import { VerificationChecklist } from "./VerificationChecklist";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { CheckCircle2, AlertTriangle } from "lucide-react";

interface BatchResultsProps {
  response: VerifyResponse;
}

export function BatchResults({ response }: BatchResultsProps) {
  const { results, batch_summary } = response;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Verification Results</h2>
        <div className="text-sm text-gray-500">
          {batch_summary.total_images} image
          {batch_summary.total_images !== 1 ? "s" : ""} processed
        </div>
      </div>

      {batch_summary.needs_review > 0 ? (
        <Alert variant="warning">
          <AlertTriangle className="h-4 w-4" />
          <AlertTitle>Review Required</AlertTitle>
          <AlertDescription>
            {batch_summary.needs_review} of {batch_summary.total_images}{" "}
            label{batch_summary.needs_review !== 1 ? "s" : ""} need
            {batch_summary.needs_review === 1 ? "s" : ""} attention.
            {batch_summary.fully_compliant > 0 && (
              <span className="ml-1">
                {batch_summary.fully_compliant} appear
                {batch_summary.fully_compliant === 1 ? "s" : ""} compliant.
              </span>
            )}
          </AlertDescription>
        </Alert>
      ) : (
        <Alert variant="success">
          <CheckCircle2 className="h-4 w-4" />
          <AlertTitle>All Labels Compliant</AlertTitle>
          <AlertDescription>
            All {batch_summary.total_images} label
            {batch_summary.total_images !== 1 ? "s" : ""} passed verification.
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6">
        {results.map((result, index) => (
          <VerificationChecklist key={`${result.filename}-${index}`} result={result} />
        ))}
      </div>
    </div>
  );
}
