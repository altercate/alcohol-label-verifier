"use client";

import { useState } from "react";
import { ImageUploader } from "@/components/ImageUploader";
import { BatchResults } from "@/components/BatchResults";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { verifyLabels, VerifyResponse } from "@/lib/api";
import { Loader2, AlertCircle, FileSearch } from "lucide-react";

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [results, setResults] = useState<VerifyResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async () => {
    if (files.length === 0) return;

    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await verifyLabels(files);
      setResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setFiles([]);
    setResults(null);
    setError(null);
  };

  return (
    <main className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <FileSearch className="h-10 w-10 text-gray-700" />
            <h1 className="text-3xl font-bold text-gray-900">
              Alcohol Label Verifier
            </h1>
          </div>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Upload alcohol label images to verify compliance. The system extracts
            text using OCR and checks for required fields including brand name,
            alcohol content, and the mandatory government warning.
          </p>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Upload Label Images</CardTitle>
            <CardDescription>
              Drag and drop label images or click to browse. Supports JPG, PNG,
              and other image formats.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ImageUploader
              files={files}
              onFilesChange={setFiles}
              disabled={isLoading}
            />
          </CardContent>
        </Card>

        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="flex gap-4 mb-6">
          <Button
            onClick={handleVerify}
            disabled={files.length === 0 || isLoading}
            className="flex-1"
            size="lg"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Verifying...
              </>
            ) : (
              <>Verify Labels</>
            )}
          </Button>
          {(results || error) && (
            <Button variant="outline" onClick={handleReset} disabled={isLoading}>
              Start Over
            </Button>
          )}
        </div>

        {results && <BatchResults response={results} />}

        <footer className="mt-12 pt-6 border-t text-center text-sm text-gray-500">
          <p>
            This is a prototype for compliance label verification using OCR.
            Results should be reviewed by a compliance agent.
          </p>
        </footer>
      </div>
    </main>
  );
}
