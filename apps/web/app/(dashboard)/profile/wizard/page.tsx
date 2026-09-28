"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Input } from "@/components/ui/input";

export default function ProfileWizard() {
  const [step, setStep] = useState(1);
  const totalSteps = 6;
  const router = useRouter();

  const handleNext = () => {
    if (step < totalSteps) setStep(step + 1);
    else router.push("/assessments");
  };

  const handlePrev = () => {
    if (step > 1) setStep(step - 1);
  };

  return (
    <div className="max-w-2xl mx-auto py-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-2">Complete Your Profile</h1>
        <Progress value={(step / totalSteps) * 100} className="h-2" />
        <p className="text-sm text-muted-foreground mt-2">Step {step} of {totalSteps}</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>
            {step === 1 && "Personal Information"}
            {step === 2 && "Academic Background"}
            {step === 3 && "Subjects & Grades"}
            {step === 4 && "Work Preferences"}
            {step === 5 && "Financial Information"}
            {step === 6 && "Location Preferences"}
          </CardTitle>
        </CardHeader>
        <CardContent className="min-h-[300px]">
          {/* Mock forms for wizard steps */}
          {step === 1 && (
            <div className="space-y-4">
              <Input label="Date of Birth" type="date" />
              <Input label="City" placeholder="New York" />
              <Input label="Country" placeholder="USA" />
            </div>
          )}
          {step > 1 && (
            <div className="flex items-center justify-center h-full text-muted-foreground">
              Form fields for step {step} goes here.
            </div>
          )}
        </CardContent>
        <CardFooter className="flex justify-between border-t p-6">
          <Button variant="outline" onClick={handlePrev} disabled={step === 1}>
            Previous
          </Button>
          <Button onClick={handleNext}>
            {step === totalSteps ? "Finish & Take Assessment" : "Next"}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
