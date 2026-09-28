import { PathwayStep } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";
import { CheckCircle2, Circle } from "lucide-react";

interface PathwayTimelineProps {
  steps: PathwayStep[];
}

export function PathwayTimeline({ steps }: PathwayTimelineProps) {
  return (
    <div className="space-y-8">
      {steps.map((step, idx) => (
        <div key={step.id} className="relative flex gap-6">
          <div className="flex flex-col items-center">
            <div className="bg-background rounded-full z-10 relative">
              <CheckCircle2 className="w-6 h-6 text-primary" />
            </div>
            {idx !== steps.length - 1 && (
              <div className="w-0.5 h-full bg-border absolute top-6" />
            )}
          </div>
          <div className="flex-1 pb-8">
            <h4 className="text-lg font-semibold">{step.title}</h4>
            <p className="text-muted-foreground mt-1">{step.description}</p>
            <div className="flex gap-4 mt-3 text-sm font-medium">
              <span className="bg-muted px-2 py-1 rounded">{step.durationMonths} months</span>
              <span className="bg-primary/10 text-primary px-2 py-1 rounded">
                Est. {formatCurrency(step.costEstimate)}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
