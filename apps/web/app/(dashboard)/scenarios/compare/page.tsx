"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { formatCurrency } from "@/lib/utils";

export default function CompareScenariosPage() {
  return (
    <div className="space-y-6">
      <PageHeader title="Compare Scenarios" />
      
      <Card>
        <CardContent className="p-0 overflow-x-auto">
          <table className="w-full text-left border-collapse min-w-[600px]">
            <thead>
              <tr>
                <th className="p-4 border-b bg-muted/50 w-1/4">Metric</th>
                <th className="p-4 border-b bg-muted/50 w-[37.5%]">Base Plan</th>
                <th className="p-4 border-b bg-muted/50 w-[37.5%] border-l-2 border-primary/20 bg-primary/5">With Tech Scholarship</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              <tr>
                <td className="p-4 font-medium text-muted-foreground">Total Budget Required</td>
                <td className="p-4">{formatCurrency(120000)}</td>
                <td className="p-4 border-l-2 border-primary/20 text-green-600 font-bold">{formatCurrency(95000)}</td>
              </tr>
              <tr>
                <td className="p-4 font-medium text-muted-foreground">Primary Pathway</td>
                <td className="p-4">Software Engineer (State Univ)</td>
                <td className="p-4 border-l-2 border-primary/20 font-bold">Software Engineer (MIT)</td>
              </tr>
              <tr>
                <td className="p-4 font-medium text-muted-foreground">Overall Feasibility</td>
                <td className="p-4 text-yellow-600">Moderate Risk</td>
                <td className="p-4 border-l-2 border-primary/20 text-green-600 font-bold">Highly Feasible</td>
              </tr>
            </tbody>
          </table>
        </CardContent>
      </Card>
      
      <div className="p-6 bg-primary/10 text-primary rounded-xl border border-primary/20">
        <h3 className="font-bold mb-2">AI Recommendation</h3>
        <p>The "With Tech Scholarship" scenario is significantly better as it allows you to attend a top-tier institution while remaining within your family's budget limit. We recommend focusing on scholarship applications to make this scenario a reality.</p>
      </div>
    </div>
  );
}
