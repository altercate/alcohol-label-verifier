"use client";

import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, X, FileImage } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface ImageUploaderProps {
  files: File[];
  onFilesChange: (files: File[]) => void;
  maxFiles?: number;
  maxSizeMB?: number;
  disabled?: boolean;
}

export function ImageUploader({
  files,
  onFilesChange,
  maxFiles = 10,
  maxSizeMB = 10,
  disabled = false,
}: ImageUploaderProps) {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      const remainingSlots = maxFiles - files.length;
      const filesToAdd = acceptedFiles.slice(0, remainingSlots);
      onFilesChange([...files, ...filesToAdd]);
    },
    [files, maxFiles, onFilesChange]
  );

  const { getRootProps, getInputProps, isDragActive, fileRejections } =
    useDropzone({
      onDrop,
      accept: {
        "image/*": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"],
      },
      maxFiles: maxFiles - files.length,
      maxSize: maxSizeMB * 1024 * 1024,
      disabled: disabled || files.length >= maxFiles,
    });

  const removeFile = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index);
    onFilesChange(newFiles);
  };

  const clearAll = () => {
    onFilesChange([]);
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={cn(
          "border-2 border-dashed rounded-xl p-8 transition-colors cursor-pointer",
          isDragActive && "border-blue-500 bg-blue-50",
          disabled || files.length >= maxFiles
            ? "border-gray-200 bg-gray-50 cursor-not-allowed"
            : "border-gray-300 hover:border-gray-400"
        )}
      >
        <input {...getInputProps()} />
        <div className="flex flex-col items-center justify-center text-center">
          <Upload
            className={cn(
              "h-12 w-12 mb-4",
              isDragActive ? "text-blue-500" : "text-gray-400"
            )}
          />
          {isDragActive ? (
            <p className="text-lg font-medium text-blue-600">
              Drop images here...
            </p>
          ) : files.length >= maxFiles ? (
            <p className="text-lg font-medium text-gray-500">
              Maximum {maxFiles} files reached
            </p>
          ) : (
            <>
              <p className="text-lg font-medium text-gray-700 mb-1">
                Drop label images here, or click to browse
              </p>
              <p className="text-sm text-gray-500">
                Accepts JPG, PNG, GIF, WebP | Max {maxFiles} images, {maxSizeMB}
                MB each
              </p>
            </>
          )}
        </div>
      </div>

      {fileRejections.length > 0 && (
        <div className="text-sm text-red-600 bg-red-50 p-3 rounded-lg">
          {fileRejections.map(({ file, errors }) => (
            <div key={file.name}>
              <span className="font-medium">{file.name}:</span>{" "}
              {errors.map((e) => e.message).join(", ")}
            </div>
          ))}
        </div>
      )}

      {files.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">
              {files.length} of {maxFiles} images selected
            </span>
            <Button variant="ghost" size="sm" onClick={clearAll}>
              Clear all
            </Button>
          </div>
          <ul className="space-y-2">
            {files.map((file, index) => (
              <li
                key={`${file.name}-${index}`}
                className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2"
              >
                <div className="flex items-center gap-2 overflow-hidden">
                  <FileImage className="h-5 w-5 text-gray-400 flex-shrink-0" />
                  <span className="text-sm text-gray-700 truncate">
                    {file.name}
                  </span>
                  <span className="text-xs text-gray-400">
                    ({(file.size / 1024 / 1024).toFixed(1)} MB)
                  </span>
                </div>
                <button
                  onClick={() => removeFile(index)}
                  className="p-1 hover:bg-gray-200 rounded"
                  aria-label="Remove file"
                >
                  <X className="h-4 w-4 text-gray-500" />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
