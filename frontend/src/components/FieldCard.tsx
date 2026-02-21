"use client";

import { CheckCircle2, XCircle, AlertTriangle } from "lucide-react";
import { FieldResult } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface FieldCardProps {
  label: string;
  result: FieldResult;
}

export function FieldCard({ label, result }: FieldCardProps) {
  const statusConfig = {
    detected: {
      icon: CheckCircle2,
      color: "text-green-600",
      bgColor: "bg-green-50",
      borderColor: "border-green-200",
      badgeVariant: "success" as const,
      badgeText: "Detected",
    },
    missing: {
      icon: XCircle,
      color: "text-red-600",
      bgColor: "bg-red-50",
      borderColor: "border-red-200",
      badgeVariant: "destructive" as const,
      badgeText: "Missing",
    },
    formatting_issue: {
      icon: AlertTriangle,
      color: "text-yellow-600",
      bgColor: "bg-yellow-50",
      borderColor: "border-yellow-200",
      badgeVariant: "warning" as const,
      badgeText: "Format Issue",
    },
  };

  const config = statusConfig[result.status];
  const Icon = config.icon;

  return (
    <div
      className={cn(
        "border rounded-lg p-4",
        config.borderColor,
        config.bgColor
      )}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 min-w-0 flex-1">
          <Icon className={cn("h-5 w-5 mt-0.5 flex-shrink-0", config.color)} />
          <div className="min-w-0 flex-1">
            <div className="font-medium text-gray-900">{label}</div>
            {result.value && (
              <div className="mt-1 text-sm text-gray-600 break-words">
                &quot;{result.value}&quot;
              </div>
            )}
            {result.issues && result.issues.length > 0 && (
              <ul className="mt-2 space-y-1">
                {result.issues.map((issue, i) => (
                  <li
                    key={i}
                    className="text-xs text-yellow-700 flex items-start gap-1"
                  >
                    <span className="font-medium">Issue:</span> {issue}
                  </li>
                ))}
              </ul>
            )}
            {result.confidence !== undefined && result.confidence !== null && (
              <div className="mt-1 text-xs text-gray-400">
                Confidence: {Math.round(result.confidence * 100)}%
              </div>
            )}
          </div>
        </div>
        <Badge variant={config.badgeVariant} className="flex-shrink-0">
          {config.badgeText}
        </Badge>
      </div>
    </div>
  );
}
