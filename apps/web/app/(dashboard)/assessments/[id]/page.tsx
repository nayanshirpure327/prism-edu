"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Card, CardContent } from "@/components/ui/card";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Clock } from "lucide-react";

export default function AssessmentTakingPage() {
  const params = useParams();
  const router = useRouter();
  const [currentQ, setCurrentQ] = useState(0);
  const totalQ = 10; // mock
  const [answers, setAnswers] = useState<Record<number, string>>({});

  const handleNext = () => {
    if (currentQ < totalQ - 1) {
      setCurrentQ(currentQ + 1);
    } else {
      // submit
      router.push(`/assessments/${params.id}/results`);
    }
  };

  const handlePrev = () => {
    if (currentQ > 0) {
      setCurrentQ(currentQ - 1);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6 py-8">
      <div className="flex items-center justify-between mb-2">
        <div>
          <h1 className="text-2xl font-bold">Aptitude Assessment</h1>
          <p className="text-muted-foreground">Question {currentQ + 1} of {totalQ}</p>
        </div>
        <div className="flex items-center gap-2 text-orange-500 font-mono text-xl bg-orange-50 px-4 py-2 rounded-lg border border-orange-200">
          <Clock className="w-5 h-5" />
          42:15
        </div>
      </div>
      
      <Progress value={((currentQ + 1) / totalQ) * 100} className="h-2" />

      <Card className="mt-8 border-2">
        <CardContent className="p-8 space-y-8">
          <h2 className="text-xl font-medium">
            If a train travels 60 miles in 1.5 hours, what is its average speed in miles per hour?
          </h2>
          
          <RadioGroup 
            value={answers[currentQ]} 
            onValueChange={(val: string) => setAnswers({ ...answers, [currentQ]: val })}
            className="space-y-4"
          >
            {["30 mph", "40 mph", "45 mph", "60 mph"].map((opt, i) => (
              <div key={i} className="flex items-center space-x-3 border p-4 rounded-lg hover:bg-muted/50 transition-colors">
                <RadioGroupItem value={opt} id={`opt-${i}`} />
                <Label htmlFor={`opt-${i}`} className="flex-1 cursor-pointer font-normal text-base">{opt}</Label>
              </div>
            ))}
          </RadioGroup>
        </CardContent>
      </Card>

      <div className="flex justify-between items-center mt-8">
        <Button variant="outline" onClick={handlePrev} disabled={currentQ === 0}>Previous</Button>
        <Button onClick={handleNext} disabled={!answers[currentQ]}>
          {currentQ === totalQ - 1 ? "Submit Assessment" : "Next Question"}
        </Button>
      </div>
    </div>
  );
}
