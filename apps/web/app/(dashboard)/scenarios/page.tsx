"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Plus, Copy, Trash2, Edit2 } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ScenariosPage() {
  const router = useRouter();
  
  const scenarios = [
    { id: "1", name: "Base Plan (No changes)", date: "2026-09-20", changes: 0 },
    { id: "2", name: "If I get the Tech Scholarship", date: "2026-09-22", changes: 1 },
    { id: "3", name: "Study in UK instead", date: "2026-09-25", changes: 2 },
  ];

  return (
    <div className="space-y-6">
      <PageHeader 
        title="What-If Simulator" 
        description="Create different scenarios by tweaking variables like budget, location, and grades."
        action={<Button><Plus className="w-4 h-4 mr-2" /> New Scenario</Button>}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {scenarios.map((scenario) => (
          <Card key={scenario.id}>
            <CardHeader>
              <CardTitle className="text-xl line-clamp-1">{scenario.name}</CardTitle>
              <p className="text-sm text-muted-foreground">Updated: {scenario.date}</p>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2 text-sm">
                <div className="p-1.5 bg-primary/10 text-primary rounded">
                  <LineChart className="w-4 h-4" />
                </div>
                <span>{scenario.changes} applied changes</span>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between border-t pt-4">
              <div className="flex gap-2">
                <Link href={`/scenarios/${scenario.id}`}>
                  <Button variant="outline" size="sm" title="Edit"><Edit2 className="w-4 h-4" /></Button>
                </Link>
                <Button variant="outline" size="sm" title="Clone"><Copy className="w-4 h-4" /></Button>
              </div>
              <Button variant="outline" size="sm" className="text-destructive hover:bg-destructive hover:text-white" title="Delete">
                <Trash2 className="w-4 h-4" />
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      {scenarios.length > 1 && (
        <div className="mt-8 flex justify-center">
          <Link href="/scenarios/compare">
            <Button size="lg" variant="secondary">Compare Scenarios Side-by-Side</Button>
          </Link>
        </div>
      )}
    </div>
  );
}
