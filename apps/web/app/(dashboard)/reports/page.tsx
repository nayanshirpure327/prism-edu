"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, Download } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <PageHeader 
        title="Reports" 
        description="Generate and download comprehensive career plan reports."
      />

      <Card className="bg-primary/5 border-primary/20">
        <CardContent className="p-8 text-center flex flex-col items-center">
          <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <FileText className="w-8 h-8 text-primary" />
          </div>
          <h2 className="text-xl font-bold mb-2">Comprehensive Career Plan Report</h2>
          <p className="text-muted-foreground max-w-lg mb-6">
            Generate a full PDF report containing your profile summary, assessment results, matched careers, pathways, cost estimates, and decision matrix analysis.
          </p>
          <Button size="lg"><FileText className="w-5 h-5 mr-2"/> Generate New Report</Button>
        </CardContent>
      </Card>

      <h3 className="text-lg font-bold mt-8">Past Reports</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <CardContent className="p-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="p-2 bg-muted rounded">
                <FileText className="w-5 h-5 text-muted-foreground" />
              </div>
              <div>
                <h4 className="font-medium">Career Plan - Sep 2026</h4>
                <p className="text-xs text-muted-foreground">Generated on 2026-09-15 • 2.4 MB</p>
              </div>
            </div>
            <Button variant="outline" size="icon"><Download className="w-4 h-4" /></Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
