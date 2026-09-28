"use client";

import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { WeightSlider } from "@/components/features/decision-matrix/WeightSlider";
import { AlertCircle } from "lucide-react";

export default function DecisionMatrixPage() {
  const [weights, setWeights] = useState({
    interest: 20,
    academic: 20,
    budget: 20,
    career: 20,
    location: 10,
    duration: 10,
  });

  const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);

  const handleWeightChange = (key: keyof typeof weights, val: number) => {
    setWeights(prev => ({ ...prev, [key]: val }));
  };

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Decision Matrix" 
        description="Evaluate your pathways objectively based on your priorities."
      />

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <Card className="lg:col-span-1 h-fit">
          <CardHeader>
            <CardTitle>Configure Weights</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className={`p-3 rounded-lg flex items-center gap-2 text-sm font-medium ${totalWeight === 100 ? 'bg-green-50 text-green-700' : 'bg-red-50 text-red-700'}`}>
              {totalWeight !== 100 && <AlertCircle className="w-4 h-4" />}
              Total: {totalWeight}% (Must be 100%)
            </div>
            
            <WeightSlider label="Interest Fit" value={weights.interest} onChange={(v) => handleWeightChange("interest", v)} />
            <WeightSlider label="Academic Fit" value={weights.academic} onChange={(v) => handleWeightChange("academic", v)} />
            <WeightSlider label="Budget Fit" value={weights.budget} onChange={(v) => handleWeightChange("budget", v)} />
            <WeightSlider label="Career Alignment" value={weights.career} onChange={(v) => handleWeightChange("career", v)} />
            <WeightSlider label="Location Fit" value={weights.location} onChange={(v) => handleWeightChange("location", v)} />
            <WeightSlider label="Duration" value={weights.duration} onChange={(v) => handleWeightChange("duration", v)} />
          </CardContent>
        </Card>

        <Card className="lg:col-span-3">
          <CardContent className="p-0 overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr>
                  <th className="p-4 border-b bg-muted/50 w-1/3">Factors</th>
                  <th className="p-4 border-b bg-muted/50 text-center">Pathway A: Software Engineer</th>
                  <th className="p-4 border-b bg-muted/50 text-center">Pathway B: Data Scientist</th>
                </tr>
              </thead>
              <tbody className="divide-y">
                <tr>
                  <td className="p-4 font-medium">Interest Fit ({weights.interest}%)</td>
                  <td className="p-4 text-center bg-green-50">9/10</td>
                  <td className="p-4 text-center bg-green-50">8/10</td>
                </tr>
                <tr>
                  <td className="p-4 font-medium">Budget Fit ({weights.budget}%)</td>
                  <td className="p-4 text-center bg-yellow-50">6/10</td>
                  <td className="p-4 text-center bg-red-50">4/10</td>
                </tr>
                <tr>
                  <td className="p-4 font-bold bg-muted/20">Weighted Total Score</td>
                  <td className="p-4 text-center font-bold text-lg bg-primary/10 text-primary">8.2 / 10</td>
                  <td className="p-4 text-center font-bold text-lg">7.5 / 10</td>
                </tr>
              </tbody>
            </table>
          </CardContent>
          <div className="p-4 text-sm text-center text-muted-foreground border-t">
            * This matrix reflects your stated preferences, not an objective ranking.
          </div>
        </Card>
      </div>
    </div>
  );
}
