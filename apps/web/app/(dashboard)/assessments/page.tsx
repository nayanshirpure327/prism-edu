"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Clock, Brain, Compass } from "lucide-react";
import Link from "next/link";

export default function AssessmentsPage() {
  const assessments = [
    {
      id: "aptitude",
      title: "Aptitude Assessment",
      description: "Measure your logical, verbal, numerical, spatial, and analytical skills to find the best career fit.",
      type: "APTITUDE",
      time: "45 mins",
      questions: 60,
      status: "COMPLETED",
      score: 85,
      icon: Brain,
    },
    {
      id: "interest",
      title: "Interest Assessment",
      description: "Discover what activities and subjects you truly enjoy to align your career with your passions.",
      type: "INTEREST",
      time: "20 mins",
      questions: 40,
      status: "PENDING",
      score: null,
      icon: Compass,
    }
  ];

  return (
    <div className="space-y-6">
      <PageHeader 
        title="Assessments" 
        description="Discover your strengths and interests to get personalized career recommendations." 
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {assessments.map((assessment) => {
          const Icon = assessment.icon;
          return (
            <Card key={assessment.id} className="flex flex-col">
              <CardHeader>
                <div className="flex justify-between items-start mb-2">
                  <div className="p-3 bg-primary/10 rounded-lg text-primary">
                    <Icon className="w-6 h-6" />
                  </div>
                  {assessment.status === "COMPLETED" ? (
                    <Badge variant="success">Completed</Badge>
                  ) : (
                    <Badge variant="outline">Pending</Badge>
                  )}
                </div>
                <CardTitle>{assessment.title}</CardTitle>
                <CardDescription>{assessment.description}</CardDescription>
              </CardHeader>
              <CardContent className="flex-1">
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Clock className="w-4 h-4" />
                    {assessment.time}
                  </div>
                  <div className="flex items-center gap-1">
                    <Brain className="w-4 h-4" />
                    {assessment.questions} Questions
                  </div>
                </div>
                {assessment.status === "COMPLETED" && (
                  <div className="mt-4 p-4 bg-muted rounded-lg">
                    <div className="text-sm font-medium">Overall Score</div>
                    <div className="text-2xl font-bold text-primary">{assessment.score}%</div>
                  </div>
                )}
              </CardContent>
              <CardFooter className="border-t pt-6 gap-3">
                {assessment.status === "COMPLETED" ? (
                  <>
                    <Link href={`/assessments/${assessment.id}/results`} className="flex-1">
                      <Button variant="outline" className="w-full">View Results</Button>
                    </Link>
                    <Link href={`/assessments/${assessment.id}`} className="flex-1">
                      <Button variant="secondary" className="w-full">Retake</Button>
                    </Link>
                  </>
                ) : (
                  <Link href={`/assessments/${assessment.id}`} className="w-full">
                    <Button className="w-full">Start Assessment</Button>
                  </Link>
                )}
              </CardFooter>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
