"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Map, Plus } from "lucide-react";
import Link from "next/link";
import { formatCurrency } from "@/lib/utils";

const pathways = [
  {
    id: "1",
    title: "Path to Software Engineer",
    careerTarget: "Software Engineer",
    compatibility: 92,
    duration: 48,
    cost: 120000,
    steps: 4
  },
  {
    id: "2",
    title: "Path to Data Scientist",
    careerTarget: "Data Scientist",
    compatibility: 85,
    duration: 60,
    cost: 150000,
    steps: 5
  }
];

export default function PathwaysPage() {
  return (
    <div className="space-y-6">
      <PageHeader 
        title="My Pathways" 
        description="Your AI-generated roadmaps to achieve your career goals."
        action={
          <Button><Plus className="w-4 h-4 mr-2" /> Generate New Pathway</Button>
        }
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {pathways.map((p) => (
          <Card key={p.id}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <CardTitle className="text-xl">{p.title}</CardTitle>
                <div className={`px-2 py-1 rounded text-sm font-bold ${p.compatibility >= 90 ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>
                  {p.compatibility}% Match
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-3 gap-4 text-center divide-x">
                <div>
                  <div className="text-sm text-muted-foreground">Steps</div>
                  <div className="font-semibold">{p.steps}</div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Duration</div>
                  <div className="font-semibold">{p.duration} mo</div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Est. Cost</div>
                  <div className="font-semibold">{formatCurrency(p.cost)}</div>
                </div>
              </div>
            </CardContent>
            <CardFooter>
              <Link href={`/pathways/${p.id}`} className="w-full">
                <Button variant="outline" className="w-full">View Details</Button>
              </Link>
            </CardFooter>
          </Card>
        ))}
      </div>
    </div>
  );
}
