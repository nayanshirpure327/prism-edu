"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { PathwayTimeline } from "@/components/features/pathways/PathwayTimeline";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { formatCurrency } from "@/lib/utils";
import { FileText, Share2 } from "lucide-react";
import Link from "next/link";

export default function PathwayDetailsPage() {
  const pathway = {
    title: "Path to Software Engineer",
    target: "Software Engineer",
    score: 92,
    totalCost: 120000,
    steps: [
      {
        id: "step1",
        pathwayId: "1",
        order: 1,
        title: "High School (Science Stream)",
        description: "Complete high school with focus on Mathematics and Physics.",
        durationMonths: 24,
        costEstimate: 0
      },
      {
        id: "step2",
        pathwayId: "1",
        order: 2,
        title: "BSc Computer Science",
        description: "4-year undergraduate degree at MIT or similar institution.",
        durationMonths: 48,
        costEstimate: 120000
      }
    ]
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start gap-4">
        <div>
          <div className="flex items-center gap-2 mb-2">
            <Badge variant="success">{pathway.score}% Compatible</Badge>
            <Badge variant="outline">Target: {pathway.target}</Badge>
          </div>
          <h1 className="text-3xl font-bold">{pathway.title}</h1>
        </div>
        <div className="flex gap-2">
          <Button variant="outline"><Share2 className="w-4 h-4 mr-2" /> Share</Button>
          <Link href="/scenarios">
            <Button>What-If Simulation</Button>
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-8">
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Timeline</CardTitle>
            </CardHeader>
            <CardContent>
              <PathwayTimeline steps={pathway.steps} />
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Estimated Cost Breakdown</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-primary mb-4">
                {formatCurrency(pathway.totalCost)}
              </div>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Tuition</span>
                  <span>{formatCurrency(80000)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Living</span>
                  <span>{formatCurrency(35000)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Other</span>
                  <span>{formatCurrency(5000)}</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-primary/5 border-primary/20">
            <CardHeader>
              <CardTitle>Funding Opportunities</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-4">
                We found 3 scholarships that match this pathway and your profile.
              </p>
              <Link href="/scholarships">
                <Button variant="outline" className="w-full bg-background">View Scholarships</Button>
              </Link>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
